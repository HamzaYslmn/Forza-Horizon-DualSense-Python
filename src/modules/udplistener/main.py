"""UDP listener for Forza Horizon telemetry.

Packet = 324 bytes; offsets verified against FH Data Out spec.
Always returns the *latest* packet (drains queued ones) so we never react
to stale telemetry.
"""
import logging
import socket
import struct

log = logging.getLogger("fhds.udp")


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
        "wheel_in_puddle_depth_fl": f(132), 
        "wheel_in_puddle_depth_fr": f(136),
        "wheel_in_puddle_depth_rl": f(140), 
        "wheel_in_puddle_depth_rr": f(144),
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
        # 232 to 244 are padding / unknown in some versions
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
        "normalized_ai_brake_difference": b(322)
    }


class UDPListener:
    """UDP listener that always returns the most recent packet."""

    def __init__(self, host: str, port: int, timeout: float = 0.5):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None

    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Small recv buffer keeps the OS from queueing many stale packets.
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(self.timeout)
        return self

    def __exit__(self, *args):
        if self.sock:
            self.sock.close()
            self.sock = None

    def recv_latest(self):
        """Block up to ``timeout`` for at least one packet, then drain the
        socket and return only the most recent one. Returns ``(pkt, addr)``
        or ``(None, None)`` on timeout."""
        try:
            pkt, addr = self.sock.recvfrom(1500)
        except socket.timeout:
            return None, None
        # Drain whatever else is already queued — we only care about the newest.
        self.sock.setblocking(False)
        try:
            while True:
                pkt, addr = self.sock.recvfrom(1500)
        except (BlockingIOError, OSError):
            pass
        finally:
            self.sock.setblocking(True)
        return pkt, addr
