"""UDP listener for Forza Horizon telemetry.

Packet = 324 bytes; offsets verified against FH Data Out spec.
Always returns the *latest* packet (drains queued ones) so I never react
to stale telemetry.
"""
import logging
import socket
import struct
from .udp_forward import UDPForwarder

log = logging.getLogger("fhds.udp")

PACKET_SIZE = 324


def parse_packet(p: bytes) -> dict:
    if len(p) < 323:
        raise ValueError(f"Packet too short: {len(p)}")
    f = lambda o: struct.unpack_from("<f", p, o)[0]  # noqa: E731
    i = lambda o: struct.unpack_from("<i", p, o)[0]  # noqa: E731
    b = lambda o: struct.unpack_from("<b", p, o)[0]  # noqa: E731
    I = lambda o: struct.unpack_from("<I", p, o)[0]  # noqa: E731
    H = lambda o: struct.unpack_from("<H", p, o)[0]  # noqa: E731

    # Format specified by the Forza Motorsport Data Out documentation
    return {
        "on": i(0) != 0,
        "timestamp_ms": I(4),
        "max_rpm": f(8),
        "idle_rpm": f(12),
        "rpm": f(16),
        "accel_x": f(20),
        "accel_y": f(24),
        "accel_z": f(28),
        "velocity_x": f(32),
        "velocity_y": f(36),
        "velocity_z": f(40),
        "angular_velocity_x": f(44),
        "angular_velocity_y": f(48),
        "angular_velocity_z": f(52),
        "yaw": f(56),
        "pitch": f(60),
        "roll": f(64),
        "norm_suspension_travel_fl": f(68),
        "norm_suspension_travel_fr": f(72),
        "norm_suspension_travel_rl": f(76),
        "norm_suspension_travel_rr": f(80),
        "tire_slip_ratio_fl": f(84),
        "tire_slip_ratio_fr": f(88),
        "tire_slip_ratio_rl": f(92),
        "tire_slip_ratio_rr": f(96),
        "wheel_rotation_speed_fl": f(100),
        "wheel_rotation_speed_fr": f(104),
        "wheel_rotation_speed_rl": f(108),
        "wheel_rotation_speed_rr": f(112),
        "wheel_on_rumble_strip_fl": i(116),
        "wheel_on_rumble_strip_fr": i(120),
        "wheel_on_rumble_strip_rl": i(124),
        "wheel_on_rumble_strip_rr": i(128),
        "wheel_in_puddle_fl": i(132),
        "wheel_in_puddle_fr": i(136),
        "wheel_in_puddle_rl": i(140),
        "wheel_in_puddle_rr": i(144),
        "surface_rumble_fl": f(148),
        "surface_rumble_fr": f(152),
        "surface_rumble_rl": f(156),
        "surface_rumble_rr": f(160),
        "tire_slip_angle_fl": f(164),
        "tire_slip_angle_fr": f(168),
        "tire_slip_angle_rl": f(172),
        "tire_slip_angle_rr": f(176),
        "tire_combined_slip_fl": f(180),
        "tire_combined_slip_fr": f(184),
        "tire_combined_slip_rl": f(188),
        "tire_combined_slip_rr": f(192),
        "suspension_travel_meters_fl": f(196),
        "suspension_travel_meters_fr": f(200),
        "suspension_travel_meters_rl": f(204),
        "suspension_travel_meters_rr": f(208),
        "car_ordinal": i(212),
        "car_class": i(216),
        "car_performance_index": i(220),
        "drive_train": i(224),
        "num_cylinders": i(228),
        # FH6 inserted 3 fields here (garbage values on older titles)
        "car_group": I(232),
        "smashable_vel_diff": f(236),
        "smashable_mass": f(240),
        "position_x": f(244),
        "position_y": f(248),
        "position_z": f(252),
        "speed": f(256) * 3.6,  # m/s to km/h
        "power": f(260),
        "torque": f(264),
        "tire_temp_fl": f(268),
        "tire_temp_fr": f(272),
        "tire_temp_rl": f(276),
        "tire_temp_rr": f(280),
        "boost": f(284),
        "fuel": f(288),
        "distance_traveled": f(292),
        "best_lap_time": f(296),
        "last_lap_time": f(300),
        "current_lap_time": f(304),
        "current_race_time": f(308),
        "lap_number": H(312),
        "race_position": p[314],
        "accel": p[315],
        "brake": p[316],
        "clutch": p[317],
        "handbrake": p[318],
        "gear": p[319],
        "steer": b(320),
        "normalized_driving_line": b(321),
        "normalized_ai_brake_difference": b(322),
    }


class UDPListener:
    """UDP listener that always returns the most recent packet.

    Uses a single dual-stack IPv6 socket (V6ONLY=0) so packets sent to
    either IPv4 or IPv6 localhost are received with no user config.
    Falls back to IPv4 if IPv6 is unavailable.
    """

    def __init__(self, host: str, port: int, timeout: float = 0.5,
                forward_to: str = "", forward_enabled: bool = True):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock: socket.socket | None = None
        self._warned_sizes: set[int] = set()
        self._fwd = UDPForwarder(forward_to, forward_enabled)

    def _open_dual_stack(self) -> socket.socket | None:
        try:
            s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)
            s.bind(("::", self.port))
            log.info("UDP listening on [::]:%d (IPv4+IPv6)", self.port)
            return s
        except OSError as e:
            log.warning("Dual-stack bind failed, falling back to IPv4: %s", e)
            return None

    def _open_ipv4(self) -> socket.socket | None:
        # MARK: return None on bind failure so __enter__ can raise with context
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)
            except OSError as e:
                log.warning("SO_RCVBUF rejected: %s", e)
            s.bind((self.host, self.port))
            log.info("UDP listening on %s:%d (IPv4)", self.host, self.port)
            return s
        except OSError as e:
            log.warning("IPv4 bind on %s:%d failed: %s", self.host, self.port, e)
            return None

    def __enter__(self):
        self.sock = self._open_dual_stack() or self._open_ipv4()
        if self.sock is None:
            raise OSError(
                f"UDP port {self.port} could not be bound (in use, blocked, or invalid host {self.host!r})"
            )
        self.sock.settimeout(self.timeout)
        self._fwd.open()
        return self

    def __exit__(self, *args):
        if self.sock:
            self.sock.close()
            self.sock = None
        self._fwd.close()

    def recv_latest(self):
        """Block up to ``timeout`` for at least one packet, then drain the
        socket and return only the most recent one. Returns ``(pkt, addr)``
        or ``(None, None)`` on timeout. Non-Forza packets (wrong size) are
        dropped with a one-time warning per distinct size."""
        try:
            pkt, addr = self.sock.recvfrom(1500)
        except socket.timeout:
            return None, None
        except OSError as e:
            # MARK: NIC change, sleep/wake, route flap - log once and skip frame
            log.warning("UDP recvfrom error: %s", e)
            return None, None
        forwarding = self._fwd.active
        if forwarding:
            self._fwd.send(pkt)
        self.sock.setblocking(False)
        try:
            while True:
                pkt, addr = self.sock.recvfrom(1500)
                if forwarding:
                    self._fwd.send(pkt)
        except (BlockingIOError, OSError):
            pass
        finally:
            self.sock.setblocking(True)
            self.sock.settimeout(self.timeout)
        if len(pkt) != PACKET_SIZE:
            if len(pkt) not in self._warned_sizes:
                self._warned_sizes.add(len(pkt))
                log.warning(
                    "Unexpected %d-byte packet from %s:%d (expected %d - may be from another app, or a new FH format)",
                    len(pkt), addr[0], addr[1], PACKET_SIZE,
                )
        return pkt, addr
