"""1:1 converter: raw adaptive-trigger HID frames -> DSX (DualSenseX) UDP instructions.

DSX drives the same DualSense firmware we'd write over HID, so each of Forza's
five frames maps to the DSX mode that reproduces it:

    raw frame            ->  DSX mode                     fidelity
    off                      OFF                          -
    rigid(force)             CustomTriggerValue / Rigid   raw resistance force 0-255
    rigid_zones(zones)       MultiplePositionFeedback     native 10x strength 0-8
    vibrate(freq, amp)       VibrateTrigger (v2)          raw pure buzz, freq 0-255
    vibrate_zones(...)       VibrateTrigger (v2)          raw pure buzz, freq 0 = sustained

Vibration uses the legacy DSX v2 `VibrateTrigger` mode: one raw 0-255 value, a
PURE motor rumble with no resistance mixed in. The v3 vibration modes are wrong
here: `Vibration` is coarse (freq 1-40, amp 1-8), and `CustomTriggerValue /
VibrateResistance` puts its 2nd byte into the *resistance force*, not amplitude
(confirmed in patmagauran/ForzaDualSense: `[freq, resistanceForce, startPos, 0..]`),
so a buzz comes out as a mushy resistance wall. VibrateTrigger has a single
intensity knob (no separate amplitude), so it runs at full firmware strength --
which is exactly the strong, raw feel we want for ABS / wheelspin / rev.

MultiplePositionFeedback is itself a 0-8 firmware effect, so the zone resistance
path loses nothing. CustomTriggerValue / Rigid keeps brake/throttle force at raw
0-255 resolution (pure resistance, no buzz).

Protocol (DSX repo, Mod System v3.1+):
    {"instructions": [{"type": <int>, "parameters": [...]}]}   type 1=TriggerUpdate, 7=Reset
    structured: [0, trigger, mode, *values]
    custom    : [0, trigger, 12(CustomTriggerValue), CustomTriggerValueMode, *7 bytes]
    vibrate   : [0, trigger, 8(VibrateTrigger), intensity 0-255]
    trigger Left=1, Right=2.
https://github.com/Paliverse/DSX/tree/main/Mod%20System%20(DSX%20v3)
"""
import logging

from modules.dualsense.adaptive_trigger import (
    M_OFF, M_RIGID, M_RIGID_ZONES, M_VIBRATE, M_VIBRATE_ZONES,
)

log = logging.getLogger("fhds.dsx")

TRIGGER_UPDATE = 1
RESET_TO_USER_SETTINGS = 7

TM_VIBRATE = 8         # VibrateTrigger (DSX v2): pure motor buzz, single value 0-255
TM_OFF = 20
TM_FEEDBACK = 25       # MultiplePositionFeedback: 10 region strengths (0-8)
TM_CUSTOM = 12         # CustomTriggerValue: raw firmware passthrough
CTV_RIGID = 1          # CustomTriggerValueMode Rigid: [start, force, 0..]

T_LEFT = 1
T_RIGHT = 2

_warned: set[int] = set()


def _u8(v):
    return max(0, min(255, int(v)))


def _instr(trigger, mode, *values):
    return {"type": TRIGGER_UPDATE, "parameters": [0, trigger, mode, *values]}


def _custom(trigger, ctv_mode, *vals):
    """CustomTriggerValue: ctv_mode + 7 raw 0-255 bytes (zero-padded)."""
    b = [_u8(v) for v in vals] + [0] * 7
    return _instr(trigger, TM_CUSTOM, ctv_mode, *b[:7])


def _unpack_zones(p):
    """Reverse adaptive_trigger._pack_zones: 6 bytes -> 10 region strengths (0-8)."""
    active = p[0] | (p[1] << 8)
    packed = p[2] | (p[3] << 8) | (p[4] << 16) | (p[5] << 24)
    return [((packed >> (3 * i)) & 0x07) + 1 if active & (1 << i) else 0
            for i in range(10)]


def _frame_to_instr(frame, trigger):
    mode, p = frame

    if mode == M_OFF:
        return _instr(trigger, TM_OFF)

    if mode == M_RIGID:                        # uniform resistance, raw force
        return _custom(trigger, CTV_RIGID, p[0], p[1]) if p[1] else _instr(trigger, TM_OFF)

    if mode == M_RIGID_ZONES:                  # per-region resistance (walls, ramps)
        zones = _unpack_zones(p)
        return _instr(trigger, TM_FEEDBACK, *zones) if any(zones) else _instr(trigger, TM_OFF)

    if mode == M_VIBRATE:                      # buzz: ABS, rev, wheelspin, idle
        return _instr(trigger, TM_VIBRATE, _u8(p[0])) if p[1] else _instr(trigger, TM_OFF)

    if mode == M_VIBRATE_ZONES:                # gear-shift kick: 0 Hz sustained push
        zones = _unpack_zones(p)
        if not any(zones):
            return _instr(trigger, TM_OFF)
        freq = p[8] if len(p) > 8 else 0       # 0 = firmware sustained kick
        return _instr(trigger, TM_VIBRATE, _u8(freq))

    if mode not in _warned:
        _warned.add(mode)
        log.warning("DSX: unmapped trigger mode 0x%02X -> OFF", mode)
    return _instr(trigger, TM_OFF)


def frames_to_packet(left, right):
    return {"instructions": [_frame_to_instr(left, T_LEFT),
                             _frame_to_instr(right, T_RIGHT)]}


def reset_packet():
    return {"instructions": [{"type": RESET_TO_USER_SETTINGS, "parameters": [0]}]}
