"""Dynamic Rev Limiter (Redline) Detector for Forza Horizon.

V5 — Optimized State Machine
- Speed gate moved to arming condition (eliminates low-speed state churn).
- Neutral gear (0, 11) ignored during shift transitions (no false disarms).
- Removed redundant _peak_rpm tracking.
"""
import logging
import time
from collections import deque
from typing import Optional, List

log = logging.getLogger(__name__)


# ── Tunables ────────────────────────────────────────────────────────────
_DEFAULTS = {
    "throttle_arm":         200,    # accel byte ≥ this to arm (~78%)
    "throttle_confirm":     160,    # accel byte ≥ this at power-cut moment (~63%)
    "throttle_release":      80,    # accel byte < this → discard armed state (~31%)

    "power_arm_min":     1000.0,    # Watts — minimal guard: engine must be producing >1kW
    "power_cut_max":        0.0,    # Watts — exact 0 means fuel cut

    "min_speed_kmh":       10.0,    # km/h — below this, won't arm (also safety discard)
    "ring_size":              3,    # frames of RPM history (3 frames ≈ 50ms at 60Hz)

    "gear_debounce_s":      0.5,    # seconds — gear must be stable for this long
    "record_cooldown_s":    1.0,    # seconds — min time between recording candidates
}

# Gears that represent transient neutral states during shifting
_NEUTRAL_GEARS = frozenset({0, 11})


def predict_rev_limiter(max_rpm: float) -> float:
    """Predicts the rev limiter from dashboard max_rpm.
    Empirical: 5000rpm → 85%, 10500rpm → 97.2%."""
    if max_rpm <= 0:
        return 0.0
    ratio = 0.85 + (max_rpm - 5000.0) * (0.972 - 0.85) / (10500.0 - 5000.0)
    ratio = max(0.80, min(0.98, ratio))
    return max_rpm * ratio


class RedlineDetector:
    """Dynamically detects the true rev limiter using power-cut detection."""

    def __init__(self):
        self._last_car_ordinal: int = -1
        self._last_car_pi: int = -1

        # Previous-frame telemetry
        self._prev_gear: int = 0

        # State machine
        self._is_armed: bool = False
        self._armed_gear: int = 0

        # Ring buffer: last N frames' RPM values
        self._rpm_ring: deque = deque(maxlen=_DEFAULTS["ring_size"])

        # Gear debounce tracking
        self._last_gear_change_time: float = 0.0
        self._current_gear: int = 0

        # Cooldown tracking
        self._last_record_time: float = 0.0

        # Clustering
        self._candidates: List[float] = []
        self._locked_redline: Optional[float] = None

    # ── Public API ──────────────────────────────────────────────────────

    def reset(self, debug_print: bool):
        """Reset all detection state (car change / tuning upgrade)."""
        self._is_armed = False
        self._armed_gear = 0
        self._rpm_ring.clear()
        self._candidates.clear()
        self._locked_redline = None
        if debug_print:
            print("[RedlineDetector] State reset, waiting for detection...")

    def update(self, t: dict, s=None) -> float:
        """Called every frame. Returns the redline value to use."""
        # ── Read settings ───────────────────────────────────────────────
        dbg   = getattr(s, "redline_debug_print", False) if s else False
        n_req = getattr(s, "redline_sample_count", 5)   if s else 5
        tol   = getattr(s, "redline_rpm_tolerance", 330.0) if s else 330.0

        max_rpm = t.get("max_rpm", 0.0)
        cur_rpm = t.get("rpm", 0.0)
        gear    = t.get("gear", 0)
        accel   = t.get("accel", 0)          # 0-255
        power   = t.get("power", 0.0)        # Watts
        idle_rpm = t.get("idle_rpm", 800.0)
        speed_kmh = t.get("speed", 0.0)      # km/h

        car_ordinal = t.get("car_ordinal", -1)
        car_pi      = t.get("car_performance_index", -1)

        now = time.monotonic()

        # ── 1. Car / tuning change detection ────────────────────────────
        ordinal_changed = (car_ordinal != self._last_car_ordinal) and car_ordinal not in (0, -1)
        pi_changed      = (car_pi != self._last_car_pi)          and car_pi not in (0, -1)

        if ordinal_changed or pi_changed:
            if dbg:
                print(f"\n[RedlineDetector] Car/tuning change detected!")
                if ordinal_changed:
                    print(f"    Ordinal: {self._last_car_ordinal} → {car_ordinal}")
                if pi_changed:
                    print(f"    PI:      {self._last_car_pi} → {car_pi}")
                print(f"    Dashboard Max RPM: {max_rpm:.0f}")
            self._last_car_ordinal = car_ordinal if car_ordinal != 0 else self._last_car_ordinal
            self._last_car_pi      = car_pi      if car_pi != 0      else self._last_car_pi
            self.reset(dbg)

        # ── 2. Gear Debounce Tracking ───────────────────────────────────
        # Only track debounced gear for REAL gears (ignore neutral 0/11)
        if gear != self._current_gear and gear not in _NEUTRAL_GEARS:
            self._current_gear = gear
            self._last_gear_change_time = now
            # Disarm only if shifted to a DIFFERENT real gear
            if self._is_armed and gear != self._armed_gear:
                if dbg:
                    print(f"[RedlineDetector] DISCARD | Gear changed "
                          f"({self._armed_gear}→{gear})")
                self._is_armed = False

        gear_is_stable = (now - self._last_gear_change_time) >= _DEFAULTS["gear_debounce_s"]

        # ── 3. Already locked → fast return ─────────────────────────────
        if self._locked_redline is not None:
            self._prev_gear = gear
            return self._locked_redline

        # ── 4. Push RPM into ring buffer ────────────────────────────────
        # Only push when in a real gear (skip neutral gaps during shifts)
        if gear not in _NEUTRAL_GEARS:
            self._rpm_ring.append(cur_rpm)

        # ── 5. State machine ────────────────────────────────────────────
        throttle_arm     = _DEFAULTS["throttle_arm"]
        throttle_confirm = _DEFAULTS["throttle_confirm"]
        throttle_release = _DEFAULTS["throttle_release"]
        power_arm_min    = _DEFAULTS["power_arm_min"]
        power_cut_max    = _DEFAULTS["power_cut_max"]
        min_speed        = _DEFAULTS["min_speed_kmh"]
        cooldown         = _DEFAULTS["record_cooldown_s"]

        if not self._is_armed:
            # ── IDLE → look for arming conditions ───────────────────────
            # Speed gate is HERE — no arming below min_speed
            if (gear >= 1
                    and gear not in _NEUTRAL_GEARS
                    and gear_is_stable
                    and accel >= throttle_arm
                    and power > power_arm_min
                    and cur_rpm > idle_rpm * 1.5
                    and speed_kmh >= min_speed):
                self._is_armed = True
                self._armed_gear = gear
                self._rpm_ring.clear()
                self._rpm_ring.append(cur_rpm)
                if dbg:
                    print(f"[RedlineDetector] ARMED | G{gear} | {speed_kmh:.0f}km/h "
                          f"| PWR {power:.0f}W | RPM {cur_rpm:.0f}")
        else:
            # ── ARMED → detect power-cut ────────────────────────────────
            record = False
            reason = ""

            is_cooled_down = (now - self._last_record_time) >= cooldown

            # For power-cut / throttle checks, use the armed gear
            # (gear might transiently be 0/11 during shift)
            effective_gear = gear if gear not in _NEUTRAL_GEARS else self._armed_gear

            # ✓ Power-cut event (exact 0W)
            if (power <= power_cut_max
                    and accel >= throttle_confirm
                    and effective_gear == self._armed_gear
                    and gear_is_stable
                    and is_cooled_down):
                record = True
                reason = f"POWER CUT (0W) gear {self._armed_gear} accel {accel}"

            # ✓ Upshift (backup signal)
            elif (gear > self._prev_gear
                  and self._prev_gear >= 1
                  and gear not in _NEUTRAL_GEARS
                  and is_cooled_down
                  and gear_is_stable):
                record = True
                reason = f"Upshift ({self._prev_gear}→{gear})"

            # ✗ Throttle released (only check when not in neutral transition)
            elif accel < throttle_release and gear not in _NEUTRAL_GEARS:
                if dbg:
                    print(f"[RedlineDetector] DISCARD | Throttle released "
                          f"(accel {accel})")
                self._is_armed = False

            # ✗ Car decelerated below min speed (safety net for braking mid-run)
            elif speed_kmh < min_speed and gear not in _NEUTRAL_GEARS:
                if dbg:
                    print(f"[RedlineDetector] DISCARD | Too slow "
                          f"({speed_kmh:.1f} km/h)")
                self._is_armed = False

            # ── Record candidate ────────────────────────────────────────
            if record:
                candidate = max(self._rpm_ring) if self._rpm_ring else cur_rpm
                self._candidates.append(candidate)
                self._is_armed = False
                self._last_record_time = now

                if dbg:
                    print(f"[RedlineDetector] CANDIDATE | {reason}")
                    print(f"    RPM ring: {[f'{v:.0f}' for v in self._rpm_ring]}")
                    print(f"    → Chosen: {candidate:.0f}")
                    print(f"    → Candidates ({len(self._candidates)}/{n_req}): "
                          f"{[f'{v:.0f}' for v in self._candidates]}")

                if len(self._candidates) >= n_req:
                    self._try_lock(dbg, n_req, tol)

        # ── 6. Save frame history ───────────────────────────────────────
        self._prev_gear = gear

        # ── 7. Return value ─────────────────────────────────────────────
        return predict_rev_limiter(max_rpm)

    # ── Clustering ──────────────────────────────────────────────────────

    def _try_lock(self, debug_print: bool, sample_count: int, rpm_tolerance: float):
        """Cluster candidates and lock if the largest cluster ≥ sample_count."""
        best_cluster: List[float] = []
        for base in self._candidates:
            cluster = [v for v in self._candidates if abs(v - base) <= rpm_tolerance]
            if len(cluster) > len(best_cluster):
                best_cluster = cluster

        if len(best_cluster) >= sample_count:
            self._locked_redline = sum(best_cluster) / len(best_cluster)
            if debug_print:
                print(f"\n{'='*50}")
                print(f"[RedlineDetector] ✓ REDLINE LOCKED!")
                print(f"    True redline: {self._locked_redline:.0f} RPM")
                print(f"    Cluster: {[f'{v:.0f}' for v in best_cluster]}")
                print(f"{'='*50}\n")
        else:
            if debug_print:
                print(f"[RedlineDetector] {len(self._candidates)} candidates, "
                      f"but cluster too scattered. Continuing...")