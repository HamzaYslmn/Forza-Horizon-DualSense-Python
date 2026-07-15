"""Per-frame loop: idle/lost handling, write-gate, once-per-second debug log."""
import logging
import time
from modules import dualsense, forzahorizon
from modules.forzahorizon import ProcessWatcher

from modules.forzahorizon.lighting import LightingController
from modules.forzahorizon.redline_detector import RedlineDetector

log = logging.getLogger("fhds")

def _max_abs(t, prefix):
    return max(abs(t[f"{prefix}_{wheel}"]) for wheel in ("fl", "fr", "rl", "rr"))

def run(ds, listener, s, stop_event=None):
    OFF = dualsense.adaptive_trigger.off()
    
    controller = forzahorizon.Controller(s)
    lighting = LightingController(s)

    redline_detector = RedlineDetector()
    
    prev_triggers = None
    last_pkt = time.monotonic()
    last_log = 0.0
    pkt_count = 0
    watcher = ProcessWatcher(s.game_process_name_contains, s.game_poll_interval_s)
    dsx_mode = getattr(ds, "is_dsx", False)

    while True:
        if stop_event is not None and stop_event.is_set():
            break
        now = time.monotonic()
        
        if s.exit_on_game_close:
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
            if idle > 1.0 and prev_triggers != (OFF, OFF):
                ds.set(OFF, OFF); prev_triggers = (OFF, OFF)
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

        # === Dynamic Redline Detection ===
        if getattr(s, "enable_dynamic_redline", True):
            try:
                # Pass settings object `s` to allow dynamic reading of sample count and tolerance
                detected_redline = redline_detector.update(t, s) 
                if detected_redline > 0:
                    t["max_rpm"] = detected_redline
            except Exception as e:
                log.debug("Redline detector failed: %s", e)

        try:
            left, right = controller.update(t, s)
        except Exception as e:
            log.warning("controller.update failed: %s", e)
            continue

        if (left, right) != prev_triggers:
            try:
                ds.set(left, right); prev_triggers = (left, right)
            except Exception as e:
                log.debug("ds.set failed: %s", e)

        if hasattr(ds, "set_lightbar"):
            try:
                led_result = lighting.update(t, now, dsx_mode=dsx_mode)
                if led_result is not None:
                    (r, g, b), player_layout, mic_state = led_result
                    
                    if getattr(s, "enable_lightbar", True):
                        ds.set_lightbar(r, g, b)
                        
                    if hasattr(ds, "set_player_led") and getattr(s, "enable_player_led", True):
                        ds.set_player_led(player_layout)
                        
                    if hasattr(ds, "set_mic_led") and getattr(s, "enable_mic_led", True):
                        ds.set_mic_led(mic_state)
            except Exception as e:
                log.debug("LED update failed: %s", e)

        if now - last_log >= 1.0:
            last_log = now
            tag = "RACE" if t["on"] else "MENU"
            slip_r = _max_abs(t, "tire_slip_ratio")
            slip_c = _max_abs(t, "tire_combined_slip")
            log.debug("[%s] %6.1f km/h | gear %d | gas %3d R=%s | brake %3d L=%s | slip %.2f combined %.2f",
                      tag, t["speed"], t["gear"], t["accel"], right, t["brake"], left, slip_r, slip_c)