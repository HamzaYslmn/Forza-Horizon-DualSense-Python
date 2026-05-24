"""Map raw DualSense HID trigger frames to DSX UDP instructions.

HID mode bytes -> closest DSX TriggerMode. CustomTriggerValue sub-modes
used for rigid and vibrate effects because they accept 0-255 values instead
of the coarse 1-8 scale of the official DSX modes.
"""

import logging

from modules.dualsense.adaptive_trigger import (
    M_OFF, M_RIGID, M_VIBRATE, M_RIGID_ZONES, M_VIBRATE_ZONES,
    M_BOW, M_GALLOP, M_MACHINE, M_WEAPON, M_WEAPON_SIMPLE,
    M_RIGID_LIMITED, M_WEAPON_LIMITED,
)

log = logging.getLogger("fhds.dsx.trigger_map")

TRIGGER_UPDATE = 1
RGB_UPDATE = 2
RESET_TO_USER_SETTINGS = 7

TM_NORMAL = 0
TM_CUSTOM_TRIGGER_VALUE = 12
TM_RESISTANCE = 13
TM_BOW = 14
TM_GALLOPING = 15
TM_SEMI_AUTOMATIC_GUN = 16
TM_AUTOMATIC_GUN = 17
TM_MACHINE = 18
TM_FEEDBACK = 21
TM_WEAPON = 22
TM_VIBRATION = 23
TM_SLOPE_FEEDBACK = 24
TM_MULTIPLE_POSITION_FEEDBACK = 25

CTV_RIGID = 1
CTV_VIBRATE_RESISTANCE = 9
CTV_VIBRATE_RESISTANCE_B = 11

T_LEFT = 1
T_RIGHT = 2

_CTV_PAD = (0, 0, 0, 0, 0)


def _pos_to_zone(pos_byte):
    return max(0, min(9, int(pos_byte) * 10 // 256))


def _unpack_zones(params):
    active = params[0] | (params[1] << 8)
    packed = params[2] | (params[3] << 8) | (params[4] << 16) | (params[5] << 24)
    zones = []
    for i in range(10):
        if active & (1 << i):
            s = ((packed >> (3 * i)) & 0x07) + 1
        else:
            s = 0
        zones.append(s)
    return zones


def _decode_zone_positions(zones_raw):
    start = end = None
    for i in range(10):
        if zones_raw & (1 << i):
            if start is None:
                start = i
            end = i
    return start or 0, max((end or start or 0), (start or 0) + 1)


def _instr(trigger_id, mode, *params):
    return {"type": TRIGGER_UPDATE, "parameters": [0, trigger_id, mode, *params]}


def _map_rigid_zones(zones, trigger_id):
    active = [(i, s) for i, s in enumerate(zones) if s > 0]
    if not active:
        return [_instr(trigger_id, TM_NORMAL)]

    if len(set(s for _, s in active)) == 1:
        return [_instr(trigger_id, TM_FEEDBACK, active[0][0], active[0][1])]

    is_non_decreasing = all(active[i][1] <= active[i + 1][1]
                           for i in range(len(active) - 1))
    if is_non_decreasing and len(active) >= 2:
        return [_instr(trigger_id, TM_SLOPE_FEEDBACK,
                       active[0][0], active[-1][0],
                       active[0][1], active[-1][1])]

    strongest = max(active, key=lambda x: (x[1], x[0]))
    return [_instr(trigger_id, TM_FEEDBACK, strongest[0], strongest[1])]


def _map_vibrate_zones(zones, freq, trigger_id):
    active = [(i, s) for i, s in enumerate(zones) if s > 0]
    if not active:
        return [_instr(trigger_id, TM_NORMAL)]
    strongest = max(active, key=lambda x: (x[1], x[0]))
    if freq == 0:
        return [_instr(trigger_id, TM_FEEDBACK, strongest[0], strongest[1])]
    strength = min(255, max(1, strongest[1]) * 30)
    return [_instr(trigger_id, TM_CUSTOM_TRIGGER_VALUE, CTV_VIBRATE_RESISTANCE_B,
                   freq, strength, *_CTV_PAD)]


def frame_to_instructions(frame, trigger_id):
    mode, params = frame

    if mode == M_OFF:
        return [_instr(trigger_id, TM_NORMAL)]

    if mode == M_RIGID:
        force = params[1]
        if force == 0:
            return [_instr(trigger_id, TM_NORMAL)]
        return [_instr(trigger_id, TM_CUSTOM_TRIGGER_VALUE, CTV_RIGID,
                       0, force, *_CTV_PAD)]

    if mode == M_VIBRATE:
        if len(params) == 2:
            freq, amp = params
        else:
            freq, amp, _pos = params
        if amp == 0:
            return [_instr(trigger_id, TM_NORMAL)]
        strength = min(255, int(amp) * 4)
        return [_instr(trigger_id, TM_CUSTOM_TRIGGER_VALUE, CTV_VIBRATE_RESISTANCE_B,
                       freq, strength, *_CTV_PAD)]

    if mode == M_RIGID_ZONES:
        zones = _unpack_zones(params[:6])
        return _map_rigid_zones(zones, trigger_id)

    if mode == M_VIBRATE_ZONES:
        zones = _unpack_zones(params[:6])
        freq = params[8] if len(params) > 8 else 0
        return _map_vibrate_zones(zones, freq, trigger_id)

    if mode == M_BOW:
        zones_raw = params[0] | (params[1] << 8)
        pair = params[2] | ((params[3] << 8) if len(params) > 3 else 0)
        start, end = _decode_zone_positions(zones_raw)
        strength = (pair & 0x07) + 1
        snap_force = ((pair >> 3) & 0x07) + 1
        return [_instr(trigger_id, TM_BOW, start, end, strength, snap_force)]

    if mode == M_GALLOP:
        zones_raw = params[0] | (params[1] << 8)
        pair = params[2]
        freq = params[3]
        start, end = _decode_zone_positions(zones_raw)
        first_foot = (pair >> 3) & 0x07
        second_foot = pair & 0x07
        return [_instr(trigger_id, TM_GALLOPING, start, end, first_foot, second_foot, freq)]

    if mode == M_MACHINE:
        zones_raw = params[0] | (params[1] << 8)
        pair = params[2]
        freq = params[3]
        period = params[4]
        start, end = _decode_zone_positions(zones_raw)
        amp_a = pair & 0x07
        amp_b = (pair >> 3) & 0x07
        return [_instr(trigger_id, TM_MACHINE, start, end, amp_a, amp_b, freq, period)]

    if mode == M_WEAPON:
        zones_raw = params[0] | (params[1] << 8)
        strength = params[2] + 1
        start, end = _decode_zone_positions(zones_raw)
        return [_instr(trigger_id, TM_WEAPON, start, end, strength)]

    if mode == M_WEAPON_SIMPLE:
        start_pos, end_pos, strength = params
        return [_instr(trigger_id, TM_SEMI_AUTOMATIC_GUN,
                       _pos_to_zone(start_pos), _pos_to_zone(end_pos),
                       max(1, min(8, strength)))]

    if mode == M_RIGID_LIMITED:
        position, strength = params
        return [_instr(trigger_id, TM_CUSTOM_TRIGGER_VALUE, CTV_RIGID,
                       position, strength, *_CTV_PAD)]

    if mode == M_WEAPON_LIMITED:
        start_pos, end_pos, strength = params
        return [_instr(trigger_id, TM_WEAPON,
                       _pos_to_zone(start_pos), _pos_to_zone(end_pos),
                       max(1, min(8, strength)))]

    log.warning("Unknown trigger mode 0x%02X, falling back to Normal", mode)
    return [_instr(trigger_id, TM_NORMAL)]


def frames_to_packet(left, right):
    instructions = frame_to_instructions(left, T_LEFT) + frame_to_instructions(right, T_RIGHT)
    return {"instructions": instructions}
