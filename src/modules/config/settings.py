"""All tunables in one place. Forces 0-255, frequencies in Hz."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Settings:
    # MARK: UDP
    udp_host: str = "127.0.0.1"               # bind address for Forza Data Out
    udp_port: int = 5300                      # match Forza HUD setting
    udp_timeout: float = 0.5                  # socket recv timeout (s)

    # MARK: Pedal shared
    pedal_value_max: int = 255                # raw pedal byte range. DO NOT CHANGE
    wall_zones: int = 2                       # firmware end-wall depth; 1=top zone only, 9=full travel

    # MARK: L2 brake resistance
    # Rigid curve: 0..wall_engage_at maps baseline..max_force, then firmware wall at 100%.
    enable_brake_resistance: bool = True
    brake_deadzone: int = 50                  # ignore pedal below this byte
    brake_baseline_force: int = 20            # force at deadzone exit
    brake_max_force: int = 80                 # peak force just before the wall
    brake_curve: float = 5.0                  # parabolic exponent; higher = softer mid, harder near wall
    brake_wall_engage_at: int = 250           # byte that triggers firmware wall. DO NOT CHANGE
    brake_wall_release_at: int = 200          # hysteresis exit byte. DO NOT CHANGE
    enable_brake_static_wall: bool = False    # optional fixed wall mid-travel
    brake_static_wall_at: int = 128           # pedal byte where the static wall sits
    brake_static_wall_force: int = 255        # static wall strength

    # MARK: L2 handbrake bonus
    enable_handbrake_bonus: bool = True
    handbrake_bonus: int = 60                 # flat extra force while handbrake is engaged

    # MARK: L2 ABS pulse
    # Vibrates when tire slip crosses thresholds under hard braking.
    enable_abs: bool = True
    abs_brake_threshold: int = 80             # min brake byte to arm
    abs_min_speed_kmh: float = 15.0           # min speed to arm
    abs_slip_ratio_threshold: float = 1.0     # per-wheel slip trigger
    abs_combined_slip_threshold: float = 1.0  # combined slip trigger
    abs_freq: int = 10                        # pulse frequency
    abs_amp: int = 20                         # pulse amplitude

    # MARK: R2 throttle resistance
    # Light rigid curve: 0..wall_engage_at maps baseline..max_force, then firmware wall at 100%.
    enable_throttle_resistance: bool = True
    accel_deadzone: int = 50                  # ignore pedal below this byte
    throttle_baseline_force: int = 0          # force at deadzone exit
    throttle_max_force: int = 8               # peak force just before the wall (lighter than brake)
    throttle_curve: float = 5.0               # parabolic exponent; higher = softer early, firmer near wall
    throttle_wall_engage_at: int = 250        # byte that triggers firmware wall. DO NOT CHANGE
    throttle_wall_release_at: int = 200       # hysteresis exit byte. DO NOT CHANGE

    # MARK: R2 speed-based throttle
    # Extra throttle resistance at low speed; fades as speed rises.
    # boost=0 means off (no extra force). Flat additive at 0 km/h, fading to normal by fade_km.
    enable_speed_throttle: bool = True
    speed_throttle_boost: int = 30            # extra force added at standstill (0 = off)
    speed_throttle_fade_km: float = 80.0     # speed where boost fully fades

    # MARK: R2 rev limiter
    # Vibrates when rpm/max_rpm exceeds the ratio; brief hold smooths rpm bounce.
    enable_rev_limiter: bool = True
    rev_limit_ratio: float = 0.93             # fraction of max_rpm to fire at
    rev_limit_freq: int = 30                  # distinct from gravel/dirt drift (15/45 Hz)
    rev_limit_amp: int = 12                   # stronger than any drift surface so the warning stands out
    rev_limit_hold_ms: float = 120.0          # min on-time per trigger

    # MARK: R2 wheelspin buzz
    # `wheelspin_amp` is the tarmac reference. Off-road / water amps scale off it
    # (water 0.5x, dirt 1.5x, gravel 2x). Surface freqs are fixed in code.
    enable_wheelspin_buzz: bool = True
    wheelspin_amp: int = 3

    # MARK: R2 idle buzz
    # Engine-idle oscillation while stopped and accelerator pressed under ~25%.
    # Single chug pattern: vibrate amp toggles between low and high every half-period.
    enable_idle_buzz: bool = True
    idle_max_speed_kmh: float = 5.0           # only while car is essentially stopped
    idle_accel_max: int = 64                  # upper byte (~25% of 255): idle fades out past this press
    idle_freq: int = 30                       # base vibrate Hz
    idle_amp_low: int = 1                     # quiet half of the cycle
    idle_amp_high: int = 30                  # loud half of the cycle
    idle_period_s: float = 0.5                # full cycle length (sec)

    # MARK: Gear shift
    # One short burst on up/downshift while moving.
    enable_gear_shift: bool = True            # buzz on R2
    enable_gear_shift_brake: bool = True      # also buzz on L2 via the wall
    gear_shift_freq: int = 10
    gear_shift_amp: int = 255
    gear_shift_duration_ms: float = 100.0     # burst length

    # MARK: System - startup pulse
    enable_startup_pulse: bool = True
    startup_pulse_force: int = 150            # one-shot force test on connect

    # MARK: System - reconnect
    # Off by default for HidHide compatibility. On = USB unplug/replug recovers without restart.
    enable_reconnect: bool = False
    reconnect_interval_s: float = 5.0         # retry cadence when disconnected

    # MARK: System - controller selection
    # Lock to a specific DualSense by serial. Empty = auto (first found).
    # Soft lock: falls back to first-found if the locked one is missing.
    # USB and BT report different serials for the same controller.
    controller_lock_serial: str = ""

    # MARK: System - updates
    check_for_updates: bool = False           # ZUV loader checks GitHub for a new release at launch

    # MARK: System - language
    # Module name in `lang/` (en, tr, zh, ja). Unknown codes fall back to English.
    language: str = "en"

    # MARK: System - auto exit
    # Closes when the game process disappears; telemetry-lost is a fallback for Task Manager kills.
    exit_on_game_close: bool = True
    game_process_name_contains: tuple = ("forza",)   # substring match, case-insensitive
    game_poll_interval_s: float = 2.0                # psutil scan cadence
    telemetry_lost_exit_s: float = 60.0              # quit if no packets for this long after first packet
