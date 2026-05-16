"""DualSense adaptive trigger effects — KISS edition.

Design rule: normal trigger forces are capped well below 255 so the trigger
usually keeps physical travel free for vibration animations. Resistance ramps
smoothly from baseline to max_force across the pedal travel — no force step
at the top, since a discontinuity in rigid-mode force makes the trigger motor
chatter when the pedal oscillates around the boundary.

Right trigger (throttle), strict priority — only one effect at a time:
    1. Gear shift  -> short vibration burst
    2. Rev limiter -> 30 Hz vibration
    3. Throttle    -> exponential rigid resistance (baseline -> max)

Left trigger (brake): telemetry tire-slip pulse under ABS-like braking,
otherwise exponential rigid resistance, baseline -> max.
Handbrake adds a flat bonus.

Every effect has an enable_* switch in settings.py.
"""

import time

# --- Raw mode bytes ---
M_OFF      = 0x05
M_RIGID    = 0x01
M_PULSE    = 0x06
M_FEEDBACK = 0x21  # MultiplePositionFeedback — per-zone static strength
M_PULSE_AB = 0x26  # Pulse_AB — per-zone strength + rhythmic kickback (vibration that keeps resistance)
RAW_MAX = 255


def _clamp(v, hi=RAW_MAX):
    return max(0, min(hi, round(v)))


# --- Effect primitives ----------------------------------------------------

def off():
    return (M_OFF, ())

def rigid(force):
    return (M_RIGID, (0, _clamp(force)))

def vibration(freq, amp):
    """Mode 0x06: (freq, amp). Firmware-defined units; tune via settings."""
    return (M_PULSE, (_clamp(freq), _clamp(amp)))

def vibration_wall(amp, freq, wall_zones):
    """Pulse_AB (0x26): rhythmic resistance that preserves the wall.

    Lower zones (10 - wall_zones) vibrate at strength `amp` (1-8); the top
    `wall_zones` (1-9) stay at max strength so the firmware wall holds
    during the buzz. One byte of frequency follows the per-zone payload."""
    a = max(1, min(8, int(amp)))
    w = max(1, min(9, int(wall_zones)))
    zones = [a] * (10 - w) + [8] * w
    active = strength = 0
    for i, s in enumerate(zones):
        if s:
            active |= 1 << i
            strength |= (s - 1) << (3 * i)
    return (M_PULSE_AB, (
        active & 0xFF, (active >> 8) & 0xFF,
        strength & 0xFF, (strength >> 8) & 0xFF, (strength >> 16) & 0xFF, (strength >> 24) & 0xFF,
        _clamp(freq), 0, 0, 0,
    ))


def _amp_to_strength(amp_byte):
    """Map a 0-255 amplitude byte (mode 0x06 scale) to 1-8 firmware strength."""
    return max(1, min(8, (max(0, int(amp_byte)) // 32) + 1))

def feedback(zones):
    """MultiplePositionFeedback: 10 per-zone strengths (0-8), firmware-enforced."""
    active = force = 0
    for i, s in enumerate(zones[:10]):
        s = max(0, min(8, int(s)))
        if s:
            active |= 1 << i
            force |= (s - 1) << (3 * i)
    return (M_FEEDBACK, (
        active & 0xFF, (active >> 8) & 0xFF,
        force & 0xFF, (force >> 8) & 0xFF, (force >> 16) & 0xFF, (force >> 24) & 0xFF,
        0, 0, 0, 0,
    ))


def _max_slip(t, prefix):
    return max(abs(t.get(f"{prefix}_{w}", 0.0)) for w in ("fl", "fr", "rl", "rr"))


# --- Brake (L2) effects ---------------------------------------------------

def abs_pulse(t, s):
    """Tire-slip vibration under hard braking, else None.
    Uses plain mode 0x06 (no wall): the brake wall would block the buzz, and
    while ABS is firing the driver should feel the simulated wheel-lock
    chatter, not a static stop."""
    if not s.enable_abs:
        return None
    if t.get("brake", 0) < s.abs_brake_threshold or t.get("speed", 0.0) < s.abs_min_speed_kmh:
        return None
    if (_max_slip(t, "tire_slip_ratio") < s.abs_slip_ratio_threshold
            and _max_slip(t, "tire_combined_slip") < s.abs_combined_slip_threshold):
        return None
    return vibration(s.abs_freq, s.abs_amp)


def _ramp(value, deadzone, baseline, max_force, curve, ceiling):
    """Generic deadzone..ceiling -> baseline..max_force curve. Below deadzone holds baseline."""
    if value < deadzone:
        return baseline
    r = min(1.0, (value - deadzone) / max(ceiling - deadzone, 1))
    return baseline + (max_force - baseline) * (r ** curve)


def brake_resistance(t, s):
    """Progressive rigid brake ramp + optional handbrake bonus."""
    handbrake = s.enable_handbrake_bonus and t.get("handbrake", 0)
    if not s.enable_brake_resistance:
        return rigid(s.handbrake_bonus) if handbrake else off()
    force = _ramp(t.get("brake", 0), s.brake_deadzone, s.brake_baseline_force,
                  s.brake_max_force, s.brake_curve, s.brake_wall_engage_at)
    if handbrake:
        force += s.handbrake_bonus
    return rigid(force)


# --- Throttle (R2) effects ------------------------------------------------

def gear_shift_burst(s):
    """Short vibration burst that keeps the wall (caller decides when it's armed)."""
    return vibration_wall(_amp_to_strength(s.gear_shift_amp), s.gear_shift_freq, s.wall_zones)


def rev_limiter_buzz(t, s):
    """Vibration above the rev-limit ratio, else None.
    Plain mode 0x06 so the buzz is at full perceptible amplitude — the
    throttle is already pinned against the wall by the time this fires."""
    if not s.enable_rev_limiter or t.get("accel", 0) < s.accel_deadzone:
        return None
    max_rpm = t.get("max_rpm", 0.0)
    rpm_r = t.get("rpm", 0.0) / max_rpm if max_rpm > 0 else 0.0
    if rpm_r <= s.rev_limit_ratio:
        return None
    return vibration(s.rev_limit_freq, s.rev_limit_amp)


def build_wall(zones):
    """Static firmware wall — top `zones` (1-9) maxed at strength 8. Built once at startup."""
    n = max(1, min(9, int(zones)))
    return feedback([0] * (10 - n) + [8] * n)


def throttle_ramp(t, s):
    """Light progressive rigid throttle ramp (same curve formula as brake)."""
    return rigid(_ramp(t.get("accel", 0), s.accel_deadzone, s.throttle_baseline_force,
                       s.throttle_max_force, s.throttle_curve, s.throttle_wall_engage_at))


# --- Priority chains ------------------------------------------------------

class TriggerAnimation:
    """Computes (left, right) trigger output from Forza Horizon telemetry each frame."""

    def __init__(self, settings):
        self._prev_gear = 0
        self._shift_until = 0.0
        self._rev_until = 0.0
        self._throttle_wall = False
        self._brake_wall = False
        self._wall = build_wall(settings.wall_zones)

    def update(self, t, s):
        if not t.get("on", False):
            return off(), off()
        return self._brake(t, s), self._throttle(t, s, time.monotonic())

    @staticmethod
    def _wall_state(value, engaged, engage_at, release_at):
        """Hysteresis: enter wall at >= engage_at, leave at < release_at."""
        if engaged:
            return value >= release_at
        return value >= engage_at

    def _brake(self, t, s):
        pulse = abs_pulse(t, s)
        if pulse:
            return pulse
        brake = t.get("brake", 0)
        self._brake_wall = self._wall_state(brake, self._brake_wall,
                                            s.brake_wall_engage_at, s.brake_wall_release_at)
        if self._brake_wall and s.enable_brake_resistance:
            return self._wall
        return brake_resistance(t, s)

    def _throttle(self, t, s, now):
        # Arm shift burst on up/downshift between valid gears while moving.
        gear, speed = t.get("gear", 0), t.get("speed", 0.0)
        if (s.enable_gear_shift and self._prev_gear > 0 and gear > 0
                and gear != self._prev_gear and speed > 3.0):
            self._shift_until = now + s.gear_shift_duration_ms / 1000.0
        self._prev_gear = gear

        if s.enable_gear_shift and now < self._shift_until:
            return gear_shift_burst(s)
        # Rev limiter: hold the buzz for `rev_limit_hold_ms` after each trigger
        # so the rpm bouncing against the limit reads as a steady pulse instead
        # of a stuttering on/off.
        buzz = rev_limiter_buzz(t, s)
        if buzz:
            self._rev_until = now + s.rev_limit_hold_ms / 1000.0
            return buzz
        if now < self._rev_until and s.enable_rev_limiter:
            return vibration(s.rev_limit_freq, s.rev_limit_amp)
        if not s.enable_throttle_resistance:
            self._throttle_wall = False
            return off()
        accel = t.get("accel", 0)
        self._throttle_wall = self._wall_state(accel, self._throttle_wall,
                                                s.throttle_wall_engage_at, s.throttle_wall_release_at)
        return self._wall if self._throttle_wall else throttle_ramp(t, s)
