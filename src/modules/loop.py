"""Per-frame loop: idle/lost handling, write-gate, once-per-second debug log."""
import logging
import time

from modules import dualsense, forzahorizon
from modules.forzahorizon import ProcessWatcher

log = logging.getLogger("fhds")


def _max_abs(t, prefix):
    return max(abs(t[f"{prefix}_{wheel}"]) for wheel in ("fl", "fr", "rl", "rr"))


def run(ds, listener, s, stop_event=None):
    OFF = dualsense.adaptive_trigger.off()
    controller = forzahorizon.Controller(s)
    prev = None
    last_pkt = time.monotonic()
    last_log = 0.0
    pkt_count = 0

    watcher = ProcessWatcher(s.game_process_name_contains, s.game_poll_interval_s)
    dsx_mode = type(ds).__name__ == "DSXClient"

    while True:
        if stop_event is not None and stop_event.is_set():
            break
        now = time.monotonic()
        if s.exit_on_game_close:
            # MARK: defensive - never let watcher errors kill the loop silently
            try:
                if watcher.should_exit():
                    log.info("Game process closed — exiting.")
                    break
            except Exception as e:
                log.warning("game-close watcher error: %s", e)

        pkt, addr = listener.recv_latest()

        if pkt is None:
            idle = now - last_pkt
            if idle > 5.0 and not getattr(listener, "lost", False):
                log.warning("No UDP packets yet — check Forza Horizon Data Out IP/port and Windows Firewall")
                listener.lost = True
            if idle > 1.0 and prev != (OFF, OFF):
                ds.set(OFF, OFF); prev = (OFF, OFF)
            # Fallback exit: telemetry was flowing, then stopped for too long
            # (game killed via Task Manager, or psutil missed the process).
            if pkt_count > 0 and idle > s.telemetry_lost_exit_s:
                log.info("Telemetry lost for %.0fs — exiting.", idle)
                break
            continue

        pkt_count += 1
        last_pkt = now
        listener.lost = False
        if pkt_count == 1:
            log.info("First packet from %s:%d (%d bytes)%s", addr[0], addr[1], len(pkt),
                     " [DSX]" if dsx_mode else "")

        try:
            t = forzahorizon.parse_packet(pkt)
        except ValueError as e:
            log.warning("Bad packet from %s:%d (%d bytes): %s", addr[0], addr[1], len(pkt), e)
            continue

        # MARK: never let a controller logic bug kill the loop - log & skip frame
        try:
            left, right = controller.update(t, s)
        except Exception as e:
            log.warning("controller.update failed: %s", e)
            continue

        if (left, right) != prev:
            try:
                ds.set(left, right); prev = (left, right)
            except Exception as e:
                # MARK: HID write can fail on disconnect; reconnect logic will retry
                log.debug("ds.set failed: %s", e)

        if now - last_log >= 1.0:
            last_log = now
            tag = "RACE" if t["on"] else "MENU"
            slip_r = _max_abs(t, "tire_slip_ratio")
            slip_c = _max_abs(t, "tire_combined_slip")
            log.debug("[%s] %6.1f km/h | gear %d | gas %3d R=%s | brake %3d L=%s | slip %.2f combined %.2f",
                      tag, t["speed"], t["gear"], t["accel"], right, t["brake"], left, slip_r, slip_c)
