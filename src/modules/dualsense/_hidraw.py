"""Direct /dev/hidraw shim — Linux fallback for the libusb-built hidapi wheel
that can't claim the gamepad interface owned by the hid-playstation driver."""
import array
import fcntl
import glob
import os


def _ioc(direction: int, type_: int, nr: int, size: int) -> int:
    # Mirrors the kernel's _IOC() macro (asm-generic/ioctl.h):
    #   dir<<30 | size<<16 | type<<8 | nr. dir bits: WRITE=1, READ=2.
    return (direction << 30) | (size << 16) | (type_ << 8) | nr


# HIDIOCGFEATURE(len) / HIDIOCSFEATURE(len): direction READ|WRITE, type 'H'.
_HID_TYPE = ord("H")
_HIDIOCSFEATURE_NR = 0x06
_HIDIOCGFEATURE_NR = 0x07


def enumerate(vendor_id: int = 0, product_id: int = 0) -> list[dict]:
    out = []
    for node in sorted(glob.glob("/dev/hidraw*")):
        try:
            with open(f"/sys/class/hidraw/{os.path.basename(node)}/device/uevent") as f:
                fields = dict(l.strip().split("=", 1) for l in f if "=" in l)
            bus, vid, pid = (int(p, 16) for p in fields["HID_ID"].split(":"))
        except (OSError, KeyError, ValueError):
            continue
        if (vendor_id and vid != vendor_id) or (product_id and pid != product_id):
            continue
        # HID_UNIQ is the controller's MAC: the hid-playstation driver
        serial = fields.get("HID_UNIQ", "").replace(":", "").lower()
        out.append({"path": node.encode(), "product_id": pid,
                    "bus_type": bus, "serial_number": serial})
    return out


class device:
    _fd = -1

    def open_path(self, path):
        self._fd = os.open(path.decode(), os.O_RDWR | os.O_NONBLOCK)

    def set_nonblocking(self, _nb): pass

    def write(self, data):
        return os.write(self._fd, bytes(data))

    def get_feature_report(self, report_id, length):
        # hidapi semantics: byte 0 of the buffer is the report id on the way in,
        # and the returned list includes that report id at index 0. The kernel
        # fills the rest via the HIDIOCGFEATURE ioctl.
        buf = array.array("B", bytes([report_id]) + bytes(length))
        fcntl.ioctl(self._fd, _ioc(3, _HID_TYPE, _HIDIOCGFEATURE_NR, len(buf)), buf, True)
        return list(buf)

    def send_feature_report(self, data):
        buf = array.array("B", bytes(data))
        return fcntl.ioctl(self._fd, _ioc(3, _HID_TYPE, _HIDIOCSFEATURE_NR, len(buf)), buf, True)

    def read(self, size, timeout_ms=0):
        try:
            return os.read(self._fd, size)
        except BlockingIOError:
            return b""

    def close(self):
        if self._fd >= 0:
            os.close(self._fd)
            self._fd = -1
