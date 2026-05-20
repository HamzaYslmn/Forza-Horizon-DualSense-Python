"""All tunables in one place. Forces 0-255, frequencies in Hz."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Settings:
    # --- UDP ---
    udp_host: str = "127.0.0.1"
    udp_port: int = 5300
    udp_timeout: float = 0.5

    # --- Shared pedal config ---
    pedal_value_max: int = 255
    wall_zones: int = 2                       # firmware wall depth: 1 = only zone 9 (lightest), 9 = whole travel walled

    # =============================================================
    # L2 — Brake pedal
    # =============================================================

    # Resistance: rigid curve 0..wall_engage_at -> baseline..max_force, firmware wall at 100%.
    enable_brake_resistance: bool = True
    brake_deadzone: int = 50
    brake_baseline_force: int = 20
    brake_max_force: int = 80                 # rigid force at brake_wall_engage_at (peak of the curve before the wall)
    brake_curve: float = 5.0                  # parabolic: light through mid travel, sharply firm near the wall
    brake_wall_engage_at: int = 250           # accel byte to switch to firmware wall
    brake_wall_release_at: int = 200          # accel byte to release the wall back to rigid curve (hysteresis)
    enable_brake_static_wall: bool = False    # Optional extra static wall
    brake_static_wall_at: int = 128           # brake byte where the static wall sits
    brake_static_wall_force: int = 255        # how hard the static wall resists (0-255)

    # Handbrake bonus: flat extra force when handbrake is engaged.
    enable_handbrake_bonus: bool = True
    handbrake_bonus: int = 60

    # ABS pulse: vibrate when tire slip telemetry crosses thresholds under hard braking.
    enable_abs: bool = True
    abs_brake_threshold: int = 80             # only pulse if we're definitely braking hard
    abs_min_speed_kmh: float = 15.0           # only pulse if we're definitely moving
    abs_slip_ratio_threshold: float = 1.0
    abs_combined_slip_threshold: float = 1.0  
    abs_freq: int = 10                        # Hz for the ABS pulse
    abs_amp: int = 20                         # raw 0-255 byte for mode 0x06 vibration amplitude

    # =============================================================
    # R2 — Gas pedal
    # =============================================================

    # Resistance: light rigid curve 0..wall_engage_at -> baseline..max_force, firmware wall at 100%.
    enable_throttle_resistance: bool = True
    accel_deadzone: int = 50
    throttle_baseline_force: int = 0
    throttle_max_force: int = 8               # rigid force at the wall threshold — much lighter than the brake
    throttle_curve: float = 5.0               # parabolic: feather-light early, slightly firmer near the wall
    throttle_wall_engage_at: int = 250        # accel byte to switch to firmware wall
    throttle_wall_release_at: int = 200       # accel byte to release the wall back to rigid (hysteresis)

    # Rev limiter: vibrate when rpm/max_rpm exceeds the ratio.
    enable_rev_limiter: bool = True
    rev_limit_ratio: float = 0.93             # fire right at the cutoff, not across the whole upper rpm range
    rev_limit_freq: int = 20
    rev_limit_amp: int = 10                   # raw 0-255 byte for mode 0x06 vibration amplitude
    rev_limit_hold_ms: float = 120.0          # hold buzz this long after each trigger so the rpm bounce doesn't stutter it

    # Wheelspin pulse: vibrate + soften R2 when drive wheels lose traction
    # under throttle. M_PULSE_AB-based; intensity scales with slip severity.
    enable_wheelspin_pulse: bool = True
    wheelspin_min_throttle: int = 50           # accel byte gate; matches accel_deadzone
    wheelspin_slip_threshold: float = 1.0      # slip_ratio at which effect just starts
    wheelspin_slip_full_scale: float = 2.0     # slip above threshold for max severity
    wheelspin_freq: int = 25                   # Hz; distinct from ABS 10 Hz for identifiability

    # Gear shift: single short vibration burst on up/downshift while moving.
    enable_gear_shift: bool = True
    enable_gear_shift_brake: bool = True
    gear_shift_freq: int = 20
    gear_shift_amp: int = 255                 # raw 0-255 byte for mode 0x06 vibration amplitude
    gear_shift_duration_ms: float = 100.0     # one shot per shift

    # =============================================================
    # System
    # =============================================================

    # Startup pulse: brief trigger buzz to confirm HID connection on launch.
    enable_startup_pulse: bool = True
    startup_pulse_force: int = 150



    # Auto-reconnect to the controller when it's missing or drops. Disabled by
    # default for HidHide compatibility — re-enumerating HID devices while a
    # HidHide cloak toggles can leave the OS holding a dead handle. Enable from
    # the Settings tab if you want USB unplug/replug to recover without
    # restarting the app.
    enable_reconnect: bool = False
    reconnect_interval_s: float = 5.0

    # Whether ZUV should check for updates at launch. Default off so the user
    # isn't prompted every run; toggle on from the top of the System tab to
    # re-enable. The toggle writes a sentinel file the ZUV loader reads on next launch.
    check_for_updates: bool = False

    # UI language code (matches a module name in the `lang` package, e.g. "en",
    # "tr", "zh", "ja"). Applied at startup; change it from the LANG tab and
    # restart to re-render the UI. Unknown codes fall back to English.
    language: str = "en"

    # Auto-exit when game closes (Windows + Linux/Proton). Telemetry-lost is a fallback for Task Manager kills.
    exit_on_game_close: bool = True
    game_process_name_contains: tuple = ("forza",)
    game_poll_interval_s: float = 2.0
    telemetry_lost_exit_s: float = 60.0
