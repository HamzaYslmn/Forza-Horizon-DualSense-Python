"""DSX (DualSenseX) UDP client - sends adaptive trigger data to DSX over UDP.

Same interface as DualSense (set/open/close/connected) so the main loop
can swap between them. When active, DSX owns the controller; this client
never touches HID directly.
"""

import json
import logging
import socket
import threading
import time

from .trigger_map import (
    TRIGGER_UPDATE, RGB_UPDATE, RESET_TO_USER_SETTINGS,
    frames_to_packet,
)
from modules.dualsense.adaptive_trigger import off, rigid

log = logging.getLogger("fhds.dsx")

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 6969


class DSXClient:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT,
                 startup_pulse_force=180, enable_startup_pulse=True):
        self._host = host
        self._port = port
        self._sock = None
        self._connected = False
        self._lock = threading.Lock()
        self._pulse_force = startup_pulse_force
        self._enable_pulse = enable_startup_pulse
        self._send_count = 0

    @property
    def connected(self) -> bool:
        return self._connected

    def open(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.settimeout(2.0)
            self._connected = True
            log.info("DSX client opened -> %s:%d", self._host, self._port)
            self._send_rgb(255, 69, 0)
            log.debug("DSX: set lightbar orange")
            if self._enable_pulse:
                self.set(rigid(self._pulse_force), rigid(self._pulse_force))
                time.sleep(0.2)
                self.set(off(), off())
                log.debug("DSX: startup pulse sent")
        except OSError as e:
            log.warning("DSX client open failed: %s", e)
            self._connected = False

    def close(self):
        if self._sock:
            try:
                self._send_reset()
                log.debug("DSX: sent ResetToUserSettings")
            except Exception:
                pass
            try:
                self._sock.close()
            except Exception:
                pass
        self._sock = None
        self._connected = False
        log.info("DSX client closed (%d packets sent)", self._send_count)

    def set(self, left, right):
        if not self._connected or self._sock is None:
            return
        with self._lock:
            try:
                packet = frames_to_packet(left, right)
                data = json.dumps(packet, separators=(",", ":")).encode("ascii")
                self._sock.sendto(data, (self._host, self._port))
                self._send_count += 1
            except Exception as e:
                log.debug("DSX send failed: %s", e)

    def _send_rgb(self, r, g, b):
        packet = {"instructions": [{"type": RGB_UPDATE, "parameters": [0, r, g, b]}]}
        data = json.dumps(packet, separators=(",", ":")).encode("ascii")
        self._sock.sendto(data, (self._host, self._port))

    def _send_reset(self):
        packet = {"instructions": [{"type": RESET_TO_USER_SETTINGS, "parameters": [0]}]}
        data = json.dumps(packet, separators=(",", ":")).encode("ascii")
        self._sock.sendto(data, (self._host, self._port))
