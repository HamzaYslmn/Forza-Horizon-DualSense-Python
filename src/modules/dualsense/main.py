import logging
import struct
import sys
import threading
import time
import zlib

# PyPI's hidapi Linux wheel uses libusb, which can't claim the gamepad interface
# (hid-playstation kernel driver owns it). Use a direct /dev/hidraw shim instead.
if sys.platform.startswith("linux"):
    from . import _hidraw as hid
else:
    import hid

from . import hidhide
from .triggers import M_RIGID, off

log = logging.getLogger("fhds.dualsense")

VENDOR_ID = 0x054C
PRODUCT_IDS = (0x0CE6, 0x0DF2)  # DualSense, DualSense Edge

# valid_flag0: 0x01 (R motor), 0x02 (L motor), 0x04 (R trigger), 0x08 (L trigger).
TRIG_FLAGS = 0x04 | 0x08

# MARK: Layout maps — byte offsets per transport
# vf1 = valid_flag1, psav = power_save_control
USB = {"rid": 0x02, "flags": 1, "vf1": 2, "psav": 10, "r": 11, "l": 22, "size": 64, "bt": False}
BT  = {"rid": 0x31, "flags": 2, "vf1": 3, "psav": 11, "r": 12, "l": 23, "size": 78, "bt": True}

# Precomputed CRC of the BT report-header byte 0xA2. zlib.crc32(data, value)
# resumes from `value`, so this lets us CRC straight off the buffer without
# allocating "\xA2" + bytes(buf[:74]) on every write.
_BT_CRC_SEED = zlib.crc32(b"\xA2")

# Cached BT MAC per hidapi path. Populated lazily by _enumerate_dualsenses
# for USB DualSenses (Windows hidapi returns an empty serial for those).
# The lock serialises the open_path/feature-read section so the I/O thread and
# the UI thread don't both try to claim the same exclusive HID handle.
_mac_cache: dict[bytes, str] = {}
_mac_cache_lock = threading.Lock()



def _enumerate_dualsenses():
    """DualSense game-pad interfaces visible to hidapi. Filtered to
    usage_page=1, usage=5 (audio/sensor interfaces share VID/PID).
    Windows hidapi returns empty serials for USB DualSenses; we backfill via HID feature report 0x09.
    When the same controller appears on both USB and BT, the BT entry is dropped (wired wins)."""
    devices = [d for d in hid.enumerate(VENDOR_ID, 0)
               if d.get("product_id") in PRODUCT_IDS
               and d.get("usage_page", 1) == 1
               and d.get("usage", 5) == 5]
    for d in devices:
        if d.get("serial_number"):
            continue
        path = d["path"]
        with _mac_cache_lock:
            mac = _mac_cache.get(path)
            if mac is None:
                dev = hid.device()
                try:
                    dev.open_path(path)
                    data = dev.get_feature_report(0x09, 64)
                except (OSError, IOError) as e:
                    log.warning("feature 0x09 read failed on %r: %s", path, e)
                    dev.close()
                    continue
                dev.close()
                # Feature 0x09 returns 20 bytes; bytes 1-6 are the controller's
                # BT MAC in little-endian. hidapi formats BT-transport serials
                # the same way (verified on hidapi-windows 0.15.0). Short reads
                # (hidapi can return [] on BT-stack timeout) are skipped so a
                # bad serial does not poison the cache.
                if len(data) < 7:
                    continue
                mac = "".join(f"{b:02x}" for b in data[6:0:-1])
                _mac_cache[path] = mac
        d["serial_number"] = mac
    # A DualSense plugged in via USB while still paired/awake on BT enumerates
    # twice with the same serial. Prefer wired so the UI shows one row and the
    # connect path picks the cable.
    wired = {d["serial_number"] for d in devices
             if d.get("serial_number") and not _is_bluetooth(d)}
    return [d for d in devices
            if not (_is_bluetooth(d) and d.get("serial_number") in wired)]


def _is_bluetooth(info):
    """Detect BT across hidapi backends.

    bus_type values seen in the wild:
      - hidapi-windows:   USB=1, Bluetooth=2
      - hidapi-libusb:    follows libusb (USB always)
      - hidapi-hidraw (Linux): BUS_USB=3, BUS_BLUETOOTH=5
    """
    bus_type = info.get("bus_type")
    if bus_type in (2, 5):
        return True
    if bus_type in (1, 3):
        return False
    path = info.get("path", b"")
    if isinstance(path, str):
        path = path.encode()
    # Linux hidraw nodes don't carry bus info in the path; fall back to USB.
    return b"BTHENUM" in path.upper() or b"BLUETOOTH" in path.upper()


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


def identify_pulse(info: dict, force: int = 180, duration_s: float = 0.2) -> bool:
    """Pulse both triggers briefly on a controller picked from a hidapi info dict.
    Best-effort; returns False if the open or write failed."""
    L = BT if _is_bluetooth(info) else USB
    dev = hid.device()
    try:
        dev.open_path(info["path"])
    except (OSError, IOError) as e:
        log.warning("identify_pulse: open_path failed on %r: %s", info.get("path"), e)
        return False
    try:
        # pulse on
        pulse = (M_RIGID, (0, force))
        buf = bytearray(L["size"])
        buf[0] = L["rid"]
        if L["bt"]:
            buf[1] = 0x02
        buf[L["flags"]] = TRIG_FLAGS
        for pos, (mode, params) in ((L["r"], pulse), (L["l"], pulse)):
            buf[pos] = mode
            buf[pos + 1:pos + 1 + len(params)] = params[:10]
        if L["bt"]:
            crc = zlib.crc32(memoryview(buf)[:74], _BT_CRC_SEED)
            struct.pack_into("<I", buf, 74, crc)
        dev.write(buf)
        time.sleep(duration_s)
        # pulse off
        rest = off()
        buf = bytearray(L["size"])
        buf[0] = L["rid"]
        if L["bt"]:
            buf[1] = 0x02
        buf[L["flags"]] = TRIG_FLAGS
        for pos, (mode, params) in ((L["r"], rest), (L["l"], rest)):
            buf[pos] = mode
            buf[pos + 1:pos + 1 + len(params)] = params[:10]
        if L["bt"]:
            crc = zlib.crc32(memoryview(buf)[:74], _BT_CRC_SEED)
            struct.pack_into("<I", buf, 74, crc)
        dev.write(buf)
        return True
    except (OSError, IOError) as e:
        log.warning("identify_pulse: write failed on %r: %s", info.get("path"), e)
        return False
    finally:
        dev.close()


class DualSense:
    """Triggers-only DualSense writer. Steam keeps rumble bits untouched.

    Resilient: starts without a controller and retries every
    ``reconnect_interval_s`` seconds. Drops writes silently while disconnected.
    """

    def __init__(
        self,
        startup_pulse_force: int = 180,
        enable_startup_pulse: bool = True,
        reconnect_interval_s: float = 5.0,
        enable_reconnect: bool = False,
        controller_lock_serial: str = "",
    ):
        self.dev = None
        self.dev_path = None
        self.lay = USB
        self._lock = threading.Lock()
        self._left = self._right = off()
        self._dirty = False
        self._running = False
        self._thread = None
        # Signalled by set() and close() so the I/O thread sleeps until a new
        # frame is ready instead of busy-polling at 1 kHz.
        self._wake = threading.Event()
        self._pulse_force = startup_pulse_force
        self._enable_startup_pulse = enable_startup_pulse
        self._reconnect_interval = reconnect_interval_s
        self._enable_reconnect = enable_reconnect
        self._ever_connected = False
        self._open_hinted = False
        self._waiting_hinted = False
        self._last_attempt = -1e9
        # Idle-input watchdog. DualSense streams input reports continuously
        # (hundreds of Hz). When the controller drops, the stream stops and
        # the nonblocking read returns empty for `_input_idle_timeout`.
        self._input_idle_timeout = 3.0
        self._last_input_at = 0.0
        # Latched mode is derived (see `persistent` property). Active only when
        # HidHide is cloaking the device AND the user opted out of reconnect.
        # Locked controller serial (empty = first-found). Persists across launches.
        self._lock_serial = controller_lock_serial

    @property
    def connected(self) -> bool:
        return self.dev is not None

    @property
    def persistent(self) -> bool:
        return (self._ever_connected
                and (hidhide.is_detected() or not self._enable_reconnect))

    def open(self):
        """Start the I/O thread. Never raises if the controller is absent."""
        log.info("HidHide: %s", "detected" if hidhide.is_detected() else "not detected")
        self._log_reconnect_mode()
        self._running = True
        self._thread = threading.Thread(target=self._io, daemon=True)
        self._thread.start()

    def _log_reconnect_mode(self) -> None:
        if hidhide.is_detected() or not self._enable_reconnect:
            log.info("Latched mode: handle held silently after connect "
                     "(HidHide detected or auto-reconnect off).")
        else:
            log.info("Reconnect mode: auto-reconnect every %.0fs after drops",
                     self._reconnect_interval)

    def close(self):
        self._running = False
        self._wake.set()
        if self._thread:
            self._thread.join(timeout=2.0)
        self._disconnect()

    def set(self, left, right):
        with self._lock:
            self._left, self._right, self._dirty = left, right, True
        self._wake.set()

    def set_reconnect_enabled(self, enabled: bool) -> None:
        """Live-toggle from the Settings tab. Wakes the I/O thread so the
        retry gate and `persistent` property re-evaluate immediately."""
        new = bool(enabled)
        if new == self._enable_reconnect:
            return
        self._enable_reconnect = new
        self._wake.set()
        if new:
            log.info("Auto-reconnect enabled - drops will retry every %.0fs.",
                     self._reconnect_interval)
        else:
            log.info("Auto-reconnect disabled%s.",
                     " (HidHide detected - device will latch after connect)" if hidhide.is_detected() else "")

    def set_reconnect_interval(self, interval_s: float) -> None:
        new = float(interval_s)
        if new == self._reconnect_interval:
            return
        self._reconnect_interval = new
        self._wake.set()
        log.info("Reconnect interval = %.1fs", new)

    def set_selection(self, lock_serial: str) -> None:
        """Store new lock serial for the next connect attempt.
        Does not disconnect; call force_reconnect() to hot-swap."""
        self._lock_serial = lock_serial

    def force_reconnect(self) -> None:
        """Drop the current handle and reopen the I/O loop's reconnect gate so
        the picker's Apply can hot-swap regardless of enable_reconnect.
        Resetting `_ever_connected` also clears persistent for one cycle."""
        self._ever_connected = False
        self._last_attempt = -1e9
        self._disconnect("user-initiated switch")
        self._wake.set()

    def _safe_write(self, buf) -> None:
        """Best-effort write — used for startup pulses, power-saver, and the
        off-pulse during disconnect, all of which run while the device may be
        about to go away."""
        try:
            self.dev.write(buf)
        except Exception:
            pass

    # MARK: connect / disconnect helpers
    def _try_connect(self) -> bool:
        devices = _enumerate_dualsenses()
        # Log enumeration deltas so we can see if the OS hides/exposes the device.
        n = len(devices)
        if n != getattr(self, "_last_enum_count", -1):
            self._last_enum_count = n
            if n == 0:
                log.info("HID enumerate: 0 DualSense interfaces visible "
                         "(controller off, cable loose, or hidden by HidHide/Steam Input).")
            else:
                summary = ", ".join(
                    f"[pid=0x{d.get('product_id', 0):04x} "
                    f"up={d.get('usage_page')} u={d.get('usage')} "
                    f"bus={d.get('bus_type')}]"
                    for d in devices
                )
                log.info("HID enumerate: %d DualSense interface(s): %s", n, summary)

        # Selection: empty list -> wait; lock match -> use it; else first device.
        if not devices:
            if not self._waiting_hinted:
                log.info("Waiting for DualSense - retrying every %.0fs", self._reconnect_interval)
                self._waiting_hinted = True
            return False
        info = None
        if self._lock_serial:
            info = next((d for d in devices
                         if d.get("serial_number") == self._lock_serial), None)
        if info is None:
            info = devices[0]
        try:
            dev = hid.device()
            dev.open_path(info["path"])
            dev.set_nonblocking(True)
        except (OSError, IOError) as e:
            if not self._open_hinted:
                _log_open_failure(e)
                log.warning("open_path failed on %r - another process likely holds the "
                            "device exclusive (Steam Input, DS4Windows, reWASD).",
                            info.get("path"))
                self._open_hinted = True
            return False
        self.dev = dev
        self.dev_path = info.get("path")
        self.lay = BT if _is_bluetooth(info) else USB
        self._open_hinted = self._waiting_hinted = False
        self._ever_connected = True
        self._last_input_at = time.monotonic()
        bus = "BT" if self.lay["bt"] else "USB"
        if self.persistent:
            log.info("DualSense connected (%s) - latched", bus)
        else:
            log.info("DualSense connected (%s)", bus)

        if self._enable_startup_pulse:
            pulse = (M_RIGID, (0, self._pulse_force))
            self._safe_write(self._build(pulse, pulse))
            time.sleep(0.2)
            self._safe_write(self._build(off(), off()))
        # MARK: Power saver — one-shot at connect
        # self._safe_write(self._build_power_saver()) # Commented out due to report discussions/27
        return True

    def _disconnect(self, reason: str = ""):
        # Latched: keep the handle, ignore transient errors. HidHide cloaks
        # input but the OS link stays valid.
        if self.persistent and self._running:
            return
        was_connected = self.dev is not None
        if was_connected:
            self._safe_write(self._build(off(), off()))
            try:
                self.dev.close()
            except Exception:
                pass
        self.dev = None
        self.dev_path = None
        if was_connected:
            suffix = f" ({reason})" if reason else ""
            if self._enable_reconnect:
                log.warning("DualSense disconnected%s — retrying every %.0fs",
                            suffix, self._reconnect_interval)
            else:
                log.warning("DualSense disconnected%s — auto-reconnect is disabled "
                            "(enable it in the Settings tab to recover automatically).",
                            suffix)

    # MARK: I/O thread — reconnect when missing, write when dirty, watchdog on idle input
    def _io(self):
        while self._running:
            now = time.monotonic()

            # --- Disconnected: throttle reconnect attempts ---
            # Initial connect always retries on the reconnect_interval — the
            # user needs the controller to come up at startup. The toggle only
            # gates *re*connects: once we've been connected at least once,
            # subsequent drops are not retried when enable_reconnect is False.
            if not self.connected:
                if self._enable_reconnect or not self._ever_connected:
                    if now - self._last_attempt >= self._reconnect_interval:
                        self._last_attempt = now
                        self._try_connect()  # logs success / waiting / open-failure itself
                self._wake.wait(0.5)
                self._wake.clear()
                continue

            # Latched (HidHide + reconnect off): handle stays valid; skip the
            # watchdog and swallow transient read/write errors.
            persistent = self.persistent

            # --- Connected: drain one input report for the liveness watchdog.
            # timeout_ms=0 forces a truly nonblocking read — set_nonblocking()
            # is unreliable on Windows Bluetooth, where read() would otherwise
            # block until the BT stack times out (~30 s after a drop).
            try:
                data = self.dev.read(self.lay["size"], timeout_ms=0)
            except OSError as e:
                if not persistent:
                    self._disconnect(f"read failed: {e}")
                    continue
                data = None
            if data:
                self._last_input_at = now
            elif not persistent and now - self._last_input_at >= self._input_idle_timeout:
                self._disconnect(f"no input for {self._input_idle_timeout:.0f}s")
                continue

            # --- Write the latest queued frame, if any ---
            with self._lock:
                dirty, left, right = self._dirty, self._left, self._right
                self._dirty = False
            if dirty:
                try:
                    n = self.dev.write(self._build(left, right))
                except Exception as e:
                    if not persistent:
                        self._disconnect(f"write failed: {e}")
                        continue
                    n = None
                if not persistent and n is not None and n <= 0:
                    self._disconnect(f"write returned {n}")
                    continue

            # Sleep until set() queues a new frame, or wake to recheck watchdogs.
            self._wake.wait(0.5)
            self._wake.clear()

    def _new_report(self):
        L = self.lay
        buf = bytearray(L["size"])
        buf[0] = L["rid"]
        if L["bt"]:
            buf[1] = 0x02
        return buf

    def _finalize_bt_crc(self, buf):
        if self.lay["bt"]:
            crc = zlib.crc32(memoryview(buf)[:74], _BT_CRC_SEED)
            struct.pack_into("<I", buf, 74, crc)

    def _build(self, left, right):
        L = self.lay
        buf = self._new_report()
        buf[L["flags"]] = TRIG_FLAGS
        for pos, (mode, params) in ((L["r"], right), (L["l"], left)):
            buf[pos] = mode
            # params elements are already clamped to 0-255 by triggers.py;
            # bytearray slice-assignment accepts a tuple of ints directly.
            buf[pos + 1:pos + 1 + len(params)] = params[:10]
        self._finalize_bt_crc(buf)
        return buf  # hidapi accepts bytearray — skip the bytes() copy.

    def _build_power_saver(self):
        """Build a minimal HID report that enables the power-save flag only."""
        L = self.lay
        buf = self._new_report()
        buf[L["vf1"]] |= 0x02          # bit 1 = POWER_SAVE_CONTROL enable
        buf[L["psav"]] |= 0x10         # bit 4 = hardware power save
        self._finalize_bt_crc(buf)
        return buf
