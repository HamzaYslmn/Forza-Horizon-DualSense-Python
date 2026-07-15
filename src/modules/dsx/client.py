"""DSX (DualSenseX) UDP client.

Drop-in for DualSense at the set/open/close/connected boundary so the loop can
swap backends. Sends adaptive-trigger data to DSX over UDP instead of writing
HID directly; while active, DSX owns the controller and this never touches HID.

UDP is fire-and-forget — DSX sends no ack — so `connected` means "socket open",
not "DSX is listening". That's the most the transport allows.
"""
import json
import logging
import socket
import threading
import time

from modules.dualsense.adaptive_trigger import off, rigid

from . import dsx_wrapper as tm

log = logging.getLogger("fhds.dsx")

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 6969


class DSXClient:
    # The loop checks this capability flag instead of sniffing the class name.
    is_dsx = True

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT,
                 startup_pulse_force=180, enable_startup_pulse=True):
        self._addr = (host, port)
        self._sock = None
        self._connected = False
        self._lock = threading.Lock()
        self._pulse_force = startup_pulse_force
        self._enable_pulse = enable_startup_pulse
        self._sent = 0

    @property
    def connected(self) -> bool:
        return self._connected

    def open(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except OSError as e:
            log.warning("DSX client open failed: %s", e)
            self._connected = False
            return
        self._connected = True
        log.info("DSX client -> %s:%d (fire-and-forget UDP, no ack)", *self._addr)
        # Only ever send trigger data — the lightbar/RGB belongs to DSX, not me.
        if self._enable_pulse:
            pulse = rigid(self._pulse_force)
            self.set(pulse, pulse)
            time.sleep(0.2)
            self.set(off(), off())

    def close(self):
        if self._sock is not None:
            self._send(tm.reset_packet())
            try:
                self._sock.close()
            except OSError:
                pass
        self._sock = None
        self._connected = False
        log.info("DSX client closed (%d packets sent)", self._sent)

    def set(self, left, right):
        self._send(tm.frames_to_packet(left, right))

    #新增灯控
    def set_lightbar(self, r: int, g: int, b: int, brightness: int = 255):
        self._send(tm.lightbar_packet(r, g, b, brightness))

    def set_player_led(self, player_number: int):
        self._send(tm.player_led_packet(player_number))

    def set_mic_led(self, state: int):
        self._send(tm.mic_led_packet(state))


    # DSX owns the device and manages its own reconnect/controller selection, so
    # the rest of the DualSense control surface is a no-op here. Implementing it
    # (rather than omitting it) lets the settings tabs call these unconditionally.
    def set_reconnect_enabled(self, enabled): pass
    def set_reconnect_interval(self, interval_s): pass
    def set_selection(self, lock_serial): pass
    def force_reconnect(self): pass

    def _send(self, packet):
        if not self._connected or self._sock is None:
            return
        data = json.dumps(packet, separators=(",", ":")).encode("ascii")
        with self._lock:
            try:
                self._sock.sendto(data, self._addr)
                self._sent += 1
            except OSError as e:
                log.debug("DSX send failed: %s", e)
