import logging
import struct
import sys
import threading
import time
import zlib

import hid

from .triggers import M_RIGID, off

log = logging.getLogger("fhds.dualsense")

VENDOR_ID = 0x054C
PRODUCT_IDS = (0x0CE6, 0x0DF2)  # DualSense, DualSense Edge

# valid_flag0: 0x01 (R motor), 0x02 (L motor), 0x04 (R trigger), 0x08 (L trigger).
# Some firmware needs motor bits set for trigger bits to be processed.
TRIG_FLAGS = 0x01 | 0x02 | 0x04 | 0x08

# MARK: Layout maps — byte offsets per transport
# vf1 = valid_flag1, psav = power_save_control
USB = {"rid": 0x02, "flags": 1, "vf1": 2, "psav": 10, "r": 11, "l": 22, "size": 64, "bt": False}
BT  = {"rid": 0x31, "flags": 2, "vf1": 3, "psav": 11, "r": 12, "l": 23, "size": 78, "bt": True}


def _find_gamepad():
    """Pick the Game Pad HID interface (usage_page=1, usage=5) or None.
    Audio/sensor interfaces share VID/PID and silently drop trigger writes."""
    devices = hid.enumerate(VENDOR_ID, 0)
    for d in devices:
        if (d.get("product_id") in PRODUCT_IDS
                and d.get("usage_page", 1) == 1
                and d.get("usage", 5) == 5):
            return d
    for d in devices:
        if d.get("product_id") in PRODUCT_IDS:
            return d
    return None


def _is_bluetooth(info):
    """Detect BT across hidapi backends.

    bus_type values seen in the wild:
      - hidapi-windows:   USB=1, Bluetooth=2
      - hidapi-libusb:    follows libusb (USB always)
      - hidapi-hidraw (Linux): BUS_USB=3, BUS_BLUETOOTH=5
    """
    bus_type = info.get("bus_type")
    if bus_type is not None:
        if bus_type in (2, 5):
            return True
        if bus_type in (1, 3):
            return False
    path = info.get("path", b"")
    if isinstance(path, str):
        path = path.encode()
    path_upper = path.upper()
    if b"BTHENUM" in path_upper or b"BLUETOOTH" in path_upper:
        return True
    # Linux hidraw nodes don't carry bus info in the path; fall back to USB.
    return False


def _log_open_failure(err) -> None:
    # hidapi's "open failed" is opaque; on Linux it almost always means the
    # hidraw node is root-only because the udev rule isn't installed.
    if sys.platform.startswith("linux"):
        log.error(
            "DualSense open failed (%s). Install the udev rule:\n"
            "  sudo cp packaging/linux/70-dualsense.rules /etc/udev/rules.d/\n"
            "  sudo udevadm control --reload-rules && sudo udevadm trigger\n"
            "Then unplug/replug (USB) or re-pair (Bluetooth).", err,
        )
    else:
        log.warning("DualSense open failed (%s) — another app may be holding it open.", err)


class DualSense:
    """Triggers-only DualSense writer. Steam keeps rumble bits untouched.

    Resilient: starts without a controller and retries every
    ``reconnect_interval_s`` seconds. Drops writes silently while disconnected.
    """

    def __init__(
        self,
        startup_pulse_force: int = 180,
        enable_startup_pulse: bool = True,
        reconnect_interval_s: float = 10.0,
    ):
        self.dev = None
        self.lay = USB
        self._lock = threading.Lock()
        self._left = self._right = off()
        self._dirty = False
        self._running = False
        self._thread = None
        self._pulse_force = startup_pulse_force
        self._enable_startup_pulse = enable_startup_pulse
        self._reconnect_interval = reconnect_interval_s
        self._connected = False
        self._open_hinted = False

    @property
    def connected(self) -> bool:
        return self._connected

    def open(self):
        """Start the I/O thread. Never raises if the controller is absent."""
        self._running = True
        self._thread = threading.Thread(target=self._io, daemon=True)
        self._thread.start()

    def close(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        self._disconnect()

    def set(self, left, right):
        with self._lock:
            self._left, self._right, self._dirty = left, right, True

    # MARK: connect / disconnect helpers
    def _try_connect(self) -> bool:
        info = _find_gamepad()
        if not info:
            return False
        try:
            dev = hid.device()
            dev.open_path(info["path"])
            dev.set_nonblocking(True)
        except (OSError, IOError) as e:
            if not self._open_hinted:
                _log_open_failure(e)
                self._open_hinted = True
            return False
        self.dev = dev
        self.lay = BT if _is_bluetooth(info) else USB
        self._connected = True
        self._open_hinted = False
        log.info("DualSense connected (%s)", "BT" if self.lay["bt"] else "USB")

        if self._enable_startup_pulse:
            try:
                pulse = (M_RIGID, (0, self._pulse_force))
                self.dev.write(self._build(pulse, pulse)); time.sleep(0.2)
                self.dev.write(self._build(off(), off()))
            except Exception:
                pass
        # MARK: Power saver — one-shot at connect
        try:
            self.dev.write(self._build_power_saver())
        except Exception:
            pass
        return True

    def _disconnect(self):
        if self.dev is not None:
            try:
                self.dev.write(self._build(off(), off()))
            except Exception:
                pass
            try:
                self.dev.close()
            except Exception:
                pass
        self.dev = None
        if self._connected:
            log.warning("DualSense disconnected — retrying every %.0fs", self._reconnect_interval)
        self._connected = False

    # MARK: I/O thread — connect, write while connected, reconnect on error
    def _io(self):
        last_attempt = -1e9
        announced_waiting = False
        while self._running:
            if not self._connected:
                now = time.monotonic()
                if now - last_attempt < self._reconnect_interval:
                    time.sleep(0.1)
                    continue
                last_attempt = now
                if self._try_connect():
                    announced_waiting = False
                    continue
                if not announced_waiting:
                    log.info("Waiting for DualSense — retrying every %.0fs", self._reconnect_interval)
                    announced_waiting = True
                continue

            try:
                try:
                    self.dev.read(self.lay["size"])  # nonblocking drain
                except OSError:
                    pass

                with self._lock:
                    if not self._dirty:
                        time.sleep(0.001)
                        continue
                    left, right, self._dirty = self._left, self._right, False

                self.dev.write(self._build(left, right))
            except Exception as e:
                log.warning("HID write failed (%s) — will reconnect", e)
                self._disconnect()

    def _build(self, left, right):
        L = self.lay
        buf = bytearray(L["size"])
        buf[0] = L["rid"]
        if L["bt"]:
            buf[1] = 0x02
        buf[L["flags"]] = TRIG_FLAGS
        for pos, (mode, params) in ((L["r"], right), (L["l"], left)):
            buf[pos] = mode
            for i, b in enumerate(params[:10]):
                buf[pos + 1 + i] = b & 0xFF
        if L["bt"]:
            struct.pack_into("<I", buf, 74, zlib.crc32(b"\xA2" + bytes(buf[:74])))
        return bytes(buf)

    def _build_power_saver(self):
        """Build a minimal HID report that enables the power-save flag only."""
        L = self.lay
        buf = bytearray(L["size"])
        buf[0] = L["rid"]
        if L["bt"]:
            buf[1] = 0x02
        buf[L["vf1"]] |= 0x02          # bit 1 = POWER_SAVE_CONTROL enable
        buf[L["psav"]] |= 0x10         # bit 4 = hardware power save
        if L["bt"]:
            struct.pack_into("<I", buf, 74, zlib.crc32(b"\xA2" + bytes(buf[:74])))
        return bytes(buf)
