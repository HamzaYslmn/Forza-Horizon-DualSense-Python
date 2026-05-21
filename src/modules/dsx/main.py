"""DSX UDP output path.

Sends adaptive trigger effects to a running DSX v3.1+ instance via JSON UDP
instead of writing HID bytes directly. Wire format: JSON-encoded Packet object,
sent ASCII-encoded to 127.0.0.1:6969 (or wherever DSX is listening).

JSON shape:
    {"instructions": [{"type": 1, "parameters": [ctrl, trigger, mode, ...params]}]}

InstructionType.TriggerUpdate = 1
Trigger.Left = 1, Trigger.Right = 2
TriggerMode enum values from Resources.cs (v3 modes: OFF=20, FEEDBACK=21, ...)
"""
import json
import logging
import os
import platform
import socket
import subprocess

from modules.dualsense.triggers import M_OFF, M_RIGID, M_PULSE, M_FEEDBACK, M_PULSE_AB

log = logging.getLogger("fhds.dsx")

# --- DSX enum constants (Resources.cs) ---
_LEFT   = 1
_RIGHT  = 2
_TRIG_UPDATE = 1   # InstructionType.TriggerUpdate

# TriggerMode enum
_TM_OFF               = 20
_TM_FEEDBACK          = 21   # start(1-9), strength(1-8)
_TM_VIBRATION         = 23   # start(1-9), amplitude(1-8), freq(1-40)
_TM_MULTI_FEEDBACK    = 25   # 10 × zone strength(0-8)
_TM_MULTI_VIBRATION   = 26   # freq(1-40), 10 × zone amplitude(0-8)

DEFAULT_PORT = 6969
_PORT_FILE_NAME = "DSX_UDP_PortNumber.txt"


# --- Port / process helpers -----------------------------------------------

def autodetect_port() -> int:
    """Read DSX UDP port from %LOCALAPPDATA%\\DSX\\DSX_UDP_PortNumber.txt.
    Falls back to DEFAULT_PORT (6969) on any error."""
    try:
        local = os.environ.get("LOCALAPPDATA", "")
        path = os.path.join(local, "DSX", _PORT_FILE_NAME)
        with open(path, encoding="utf-8") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return DEFAULT_PORT


def is_dsx_running() -> bool:
    """Return True if DSX.exe is in the process list (Windows only)."""
    if platform.system() != "Windows":
        return False
    try:
        r = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq DSX.exe", "/NH"],
            capture_output=True, text=True, timeout=3,
        )
        return "DSX.exe" in r.stdout
    except Exception:
        return False


# --- HID-frame → DSX translation ------------------------------------------

def _decode_zone_strengths(params) -> list:
    """Decode packed active/force bitmasks from feedback() / vibration_wall()
    back to a list of 10 zone strength values (0-8)."""
    if len(params) < 6:
        return [0] * 10
    active  = params[0] | (params[1] << 8)
    packed  = params[2] | (params[3] << 8) | (params[4] << 16) | (params[5] << 24)
    zones = []
    for i in range(10):
        if active & (1 << i):
            zones.append(((packed >> (3 * i)) & 0x7) + 1)
        else:
            zones.append(0)
    return zones


def _frame_to_instruction_params(mode: int, params, trigger_side: int) -> list:
    """Translate one HID trigger frame to the DSX instruction parameters list
    (everything after the controller-index field)."""
    if mode == M_OFF:
        return [trigger_side, _TM_OFF]

    if mode == M_RIGID:
        # params = (0, force_byte)
        force = int(params[1]) if len(params) > 1 else 0
        strength = max(1, min(8, (force // 32) + 1))
        return [trigger_side, _TM_FEEDBACK, 1, strength]

    if mode == M_PULSE:
        # params = (freq_byte, amp_byte)
        freq = int(params[0]) if params else 0
        amp  = int(params[1]) if len(params) > 1 else 0
        dsx_amp  = max(1, min(8,  (amp  // 32) + 1))
        dsx_freq = max(1, min(40, freq))
        return [trigger_side, _TM_VIBRATION, 1, dsx_amp, dsx_freq]

    if mode == M_FEEDBACK:
        zones = _decode_zone_strengths(params)
        return [trigger_side, _TM_MULTI_FEEDBACK] + zones

    if mode == M_PULSE_AB:
        zones = _decode_zone_strengths(params)
        raw_freq = int(params[6]) if len(params) > 6 else 1
        dsx_freq = max(1, min(40, raw_freq))
        return [trigger_side, _TM_MULTI_VIBRATION, dsx_freq] + zones

    # Unknown mode — fall back to OFF
    return [trigger_side, _TM_OFF]


def build_packet_bytes(ctrl_idx: int, left_frame, right_frame) -> bytes:
    """Build the UDP payload for a pair of trigger frames."""
    l_params = _frame_to_instruction_params(left_frame[0],  left_frame[1],  _LEFT)
    r_params = _frame_to_instruction_params(right_frame[0], right_frame[1], _RIGHT)
    packet = {
        "instructions": [
            {"type": _TRIG_UPDATE, "parameters": [ctrl_idx] + l_params},
            {"type": _TRIG_UPDATE, "parameters": [ctrl_idx] + r_params},
        ]
    }
    return json.dumps(packet, separators=(",", ":")).encode("ascii")


# --- Sender ---------------------------------------------------------------

class DSXSender:
    """Fire-and-forget UDP sender to DSX v3.1+.

    Opened once; survives DSX restarts (UDP is connectionless). send() is
    best-effort: failures are logged at DEBUG level so they never kill the loop.
    """

    def __init__(self, host: str, port: int, controller_index: int = 0):
        self.host = host
        self.port = port
        self.controller_index = controller_index
        self._sock: socket.socket | None = None
        self._addr: tuple | None = None

    def open(self) -> None:
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._addr = (self.host, self.port)
            log.info("DSX sender ready → %s:%d  controller_index=%d",
                     self.host, self.port, self.controller_index)
        except OSError as e:
            log.error("DSX sender open failed: %s", e)

    def close(self) -> None:
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None
        log.debug("DSX sender closed")

    def send(self, left, right) -> None:
        if self._sock is None:
            return
        try:
            data = build_packet_bytes(self.controller_index, left, right)
            self._sock.sendto(data, self._addr)
        except Exception as e:
            log.debug("DSX send error: %s", e)

    def update_endpoint(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self._addr = (host, port)
        log.info("DSX endpoint updated → %s:%d", host, port)
