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
# Some firmware needs motor bits set for trigger bits to be processed.
TRIG_FLAGS = 0x01 | 0x02 | 0x04 | 0x08

# MARK: Layout maps — byte offsets per transport
# vf1 = valid_flag1, psav = power_save_control
USB = {"rid": 0x02, "flags": 1, "vf1": 2, "psav": 10, "r": 11, "l": 22, "size": 64, "bt": False}
BT  = {"rid": 0x31, "flags": 2, "vf1": 3, "psav": 11, "r": 12, "l": 23, "size": 78, "bt": True}

# Precomputed CRC of the BT report-header byte 0xA2. zlib.crc32(data, value)
# resumes from `value`, so this lets us CRC straight off the buffer without
# allocating "\xA2" + bytes(buf[:74]) on every write.
_BT_CRC_SEED = zlib.crc32(b"\xA2")

# Cache: hidapi path (bytes) -> derived BT MAC hex string (12 chars, lowercase).
# Used by _read_mac to avoid re-opening the same device on every enumeration.
# Only successful reads are cached; failures retry next time the path is seen.
_mac_cache: dict[bytes, str] = {}



def _enumerate_dualsenses():
    """All DualSense game-pad interfaces visible to hidapi
    (VENDOR_ID + known PRODUCT_IDS, usage_page=1, usage=5).

    Audio/sensor interfaces share VID/PID and silently drop trigger writes,
    so we filter them here once instead of at every call site.

    Windows hidapi quirk: the USB-side HID interface does not expose a serial
    string. We mitigate by reading the BT MAC via HID feature report 0x09
    (a Sony-documented feature) and using it as the canonical serial when
    hidapi returns empty. The MAC matches the BT-transport hidapi serial
    for the same physical controller, giving a single cross-transport identity
    so picker locks survive USB<->BT transport switches."""
    devices = [d for d in hid.enumerate(VENDOR_ID, 0)
               if d.get("product_id") in PRODUCT_IDS
               and d.get("usage_page", 1) == 1
               and d.get("usage", 5) == 5]
    for d in devices:
        if not d.get("serial_number"):
            mac = _read_mac(d)
            if mac:
                d["serial_number"] = mac
    return devices


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


def _read_mac(info: dict) -> str:
    """Derive a stable per-controller identity from HID feature report 0x09.

    Feature 0x09 returns a 20-byte payload; bytes 1-6 are the controller's
    BT MAC in little-endian. hidapi formats BT-transport serial_number strings
    as the same MAC in the same byte order, lowercase hex without separators
    (verified on hidapi-windows 0.15.0 against a paired DualSense). Injecting
    the derived MAC into devices with empty hidapi-serial gives a single
    identifier per physical controller, consistent across USB and BT transports.

    Best-effort: returns '' if open or feature read failed (controller will
    render as non-selectable in the picker, matching pre-fix behavior).
    Successful reads are cached by path so we only open once per device.
    Cache misses retry on the next call so transient open-blocked errors
    self-heal."""
    path = info.get("path")
    if not path:
        return ""
    cached = _mac_cache.get(path)
    if cached:
        return cached
    dev = hid.device()
    try:
        dev.open_path(path)
    except (OSError, IOError) as e:
        log.warning("_read_mac: open_path failed on %r: %s", path, e)
        return ""
    try:
        data = dev.get_feature_report(0x09, 64)
    except (OSError, IOError) as e:
        log.warning("_read_mac: feature 0x09 read failed on %r: %s", path, e)
        return ""
    finally:
        try:
            dev.close()
        except Exception:
            pass
    if len(data) < 7 or data[0] != 0x09:
        log.warning("_read_mac: unexpected feature 0x09 payload on %r: len=%d id=0x%02x",
                    path, len(data), data[0] if data else -1)
        return ""
    mac = "".join(f"{b:02x}" for b in data[6:0:-1])
    _mac_cache[path] = mac
    log.info("derived BT MAC for DualSense (%s): %s",
             "BT" if _is_bluetooth(info) else "USB", mac)
    return mac


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


def _resolve_target(devices, lock_serial, session_serial, transport_pref):
    """Selection decision tree. Pure. Returns one of:
        ("device", info)    -> attach to this device
        ("prompt", devices) -> ask the user; devices is the unresolved set
        ("none",   None)    -> no devices visible at all

    Priority within multi-device scenarios:
      1. lock_serial (persistent, soft: missing falls through to auto)
      2. session_serial (set by the modal, cleared on process exit)
      3. transport_pref ("bt" / "usb", soft: only applied when transports differ)
      4. prompt the user
    """
    if not devices:
        return ("none", None)
    if len(devices) == 1:
        return ("device", devices[0])
    if lock_serial:
        hit = next((d for d in devices
                    if d.get("serial_number") == lock_serial), None)
        if hit:
            return ("device", hit)
    if session_serial:
        hit = next((d for d in devices
                    if d.get("serial_number") == session_serial), None)
        if hit:
            return ("device", hit)
    transports = {("bt" if _is_bluetooth(d) else "usb") for d in devices}
    if transport_pref in ("bt", "usb") and len(transports) > 1:
        candidates = [d for d in devices
                      if ("bt" if _is_bluetooth(d) else "usb") == transport_pref]
        if len(candidates) == 1:
            return ("device", candidates[0])
        return ("prompt", candidates)
    return ("prompt", devices)


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
        controller_transport_preference: str = "auto",
        headless: bool = False,
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
        # HidHide-persistent: once True, _disconnect() is a no-op and the I/O
        # loop never reconnects. Latched on first successful connect when
        # HidHide is detected; never cleared.
        self._persistent = False
        # Selection state. _lock_serial and _transport_pref come from settings
        # and survive across launches. _session_serial is set only by the
        # modal prompt callback and is cleared on process exit. _pending_prompt
        # is None until the resolver hits a tie the TUI must arbitrate; the
        # TUI polls it via a set_interval watcher and pushes the modal.
        self._lock_serial = controller_lock_serial
        self._transport_pref = controller_transport_preference
        self._session_serial = ""
        self._pending_prompt = None
        # In headless mode the resolver falls through ("prompt", ...) to
        # first-found with a warning; there is no UI to render the modal.
        self._headless = headless

    @property
    def connected(self) -> bool:
        return self.dev is not None

    def open(self):
        """Start the I/O thread. Never raises if the controller is absent."""
        log.info("HidHide: %s", "detected" if hidhide.is_detected() else "not detected")
        self._log_reconnect_mode()
        self._running = True
        self._thread = threading.Thread(target=self._io, daemon=True)
        self._thread.start()

    def _log_reconnect_mode(self) -> None:
        if hidhide.is_detected():
            log.info("HidHide detected - persistent mode will engage after first connect "
                     "(reconnect setting bypassed; initial connect retries every %.0fs)",
                     self._reconnect_interval)
        elif self._enable_reconnect:
            log.info("Reconnect mode: auto-reconnect every %.0fs after drops",
                     self._reconnect_interval)
        else:
            log.info("Reconnect mode: disabled — initial connect retries every %.0fs, "
                     "but drops will not auto-recover (toggle in Settings tab)",
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
        """Live-toggle from the Settings tab. Wakes the I/O thread so a
        disconnected loop re-checks the retry gate immediately."""
        new = bool(enabled)
        if new == self._enable_reconnect:
            return
        self._enable_reconnect = new
        self._wake.set()
        if self._persistent:
            log.info("Auto-reconnect %s — HidHide persistent mode is active and overrides this.",
                     "enabled" if new else "disabled")
        elif new:
            log.info("Auto-reconnect enabled — will retry every %.0fs after drops.",
                     self._reconnect_interval)
        else:
            log.info("Auto-reconnect disabled — drops will not auto-recover until re-enabled.")

    def set_reconnect_interval(self, interval_s: float) -> None:
        new = float(interval_s)
        if new == self._reconnect_interval:
            return
        self._reconnect_interval = new
        self._wake.set()
        log.info("Reconnect interval = %.1fs", new)

    def set_selection(self, lock_serial: str, transport_pref: str) -> None:
        """Settings-changed hook called by the TUI when the user edits the
        controller lock or transport preference. Stores the values for use on
        the next connect attempt; does not disconnect. Call force_reconnect()
        to hot-swap an already-attached controller."""
        self._lock_serial = lock_serial
        self._transport_pref = transport_pref

    def pick_serial(self, serial: str) -> None:
        """Modal prompt callback. Writes the session pick (not persisted) and
        wakes the I/O thread so _try_connect re-runs immediately."""
        self._session_serial = serial
        self._pending_prompt = None
        self._wake.set()

    def force_reconnect(self) -> None:
        """User-initiated reconnect. Drops the current handle and overrides
        the HidHide-persistent latch for one cycle so the System tab's Apply
        button can hot-swap to a different controller mid-session. The latch
        re-applies on the next successful connect if HidHide is still detected."""
        self._persistent = False
        self._disconnect("user-initiated switch")
        self._wake.set()

    @property
    def pending_prompt(self):
        """Candidate device list the TUI should render in the modal, or None
        when no prompt is pending. Polled by TriggerTUI._watch_prompt."""
        return self._pending_prompt

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
                    f"[{'BT' if _is_bluetooth(d) else 'USB'} "
                    f"sn={d.get('serial_number') or '?'}]"
                    for d in devices
                )
                log.info("HID enumerate: %d DualSense interface(s): %s", n, summary)

        kind, payload = _resolve_target(
            devices,
            self._lock_serial,
            self._session_serial,
            self._transport_pref,
        )
        if kind == "none":
            if not self._waiting_hinted:
                log.info("Waiting for DualSense - retrying every %.0fs", self._reconnect_interval)
                self._waiting_hinted = True
            return False
        if kind == "prompt":
            if self._headless:
                log.warning(
                    "Multiple DualSenses visible and no rule resolves the tie; "
                    "attaching to first-found (%s sn=%s). Set "
                    "controller_lock_serial or controller_transport_preference "
                    "to choose deterministically.",
                    "BT" if _is_bluetooth(payload[0]) else "USB",
                    payload[0].get("serial_number") or "?",
                )
                info = payload[0]
            else:
                self._pending_prompt = payload
                if not self._waiting_hinted:
                    log.info("Waiting for user to pick a DualSense from %d candidates.",
                             len(payload))
                    self._waiting_hinted = True
                return False
        else:  # ("device", info)
            info = payload
        self._pending_prompt = None
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
        if hidhide.is_detected() and not self._persistent:
            self._persistent = True
            log.info("DualSense connected (%s) - persistent mode latched (HidHide present)",
                     "BT" if self.lay["bt"] else "USB")
        else:
            log.info("DualSense connected (%s)", "BT" if self.lay["bt"] else "USB")

        if self._enable_startup_pulse:
            pulse = (M_RIGID, (0, self._pulse_force))
            self._safe_write(self._build(pulse, pulse))
            time.sleep(0.2)
            self._safe_write(self._build(off(), off()))
        # MARK: Power saver — one-shot at connect
        # self._safe_write(self._build_power_saver()) # Commented out due to report discussions/27
        return True

    def _disconnect(self, reason: str = ""):
        # HidHide-persistent: keep the handle, ignore transient errors forever.
        if self._persistent and self._running:
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

            # HidHide-persistent mode: once we've connected and HidHide is on
            # the system, never tear the handle down — HidHide can cloak the
            # device mid-session and the OS link stays put. Treat read/write
            # hiccups as transient and skip the idle-input watchdog.
            persistent = self._persistent

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
