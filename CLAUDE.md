# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Forza Horizon DualSense adaptive triggers — reads Forza Horizon telemetry over UDP and drives DualSense controller trigger effects via HID. Steam's rumble stays intact; only trigger bytes are touched.

## Run / Build

```bash
# Dev (no bundle)
cd src
uv sync
uv run main.py                  # GUI (default)
uv run main.py --tui             # Textual TUI
uv run main.py --headless        # No UI, console logs only
uv run main.py --debug           # Verbose per-packet logs
uv run main.py --host ::1 --port 5300

# Build the zuv bundle (same as CI)
uvx zuv build src -o app/fhds.zuv.py --update-repo HamzaYslmn/Forza-Horizon-DualSense-Python
# Drop --update-repo for local-only iteration

# Lint
uv run ruff check src/
```

Python >=3.13 required. Dependencies: customtkinter, textual, hidapi, psutil, pillow, pystray, dotenv.

## Architecture

```
FH UDP 5300 → parse_packet → Controller.update → (left, right) → DualSense.set (state-change write) → HID
```

### Key modules

- `src/main.py` — entry point: CLI args, settings load, dispatches to GUI/TUI/headless
- `src/modules/config/settings.py` — `@dataclass Settings`: ALL tunables live here, never elsewhere
- `src/modules/config/preferences.py` — JSON persistence; globals vs per-profile fields split by `GLOBAL_FIELDS`
- `src/modules/config/profiles.py` — named profile CRUD + share-code import/export
- `src/modules/loop.py` — per-frame driver: drain UDP, parse, compute effects, state-change write
- `src/modules/forzahorizon/udp_listener.py` — 324-byte FH packet parser, dual-stack IPv6 socket
- `src/modules/forzahorizon/effects.py` — `Controller` (L2/R2 priority chains) + `TriggerAnimations` (ABS, gear shift, rev limiter, wheelspin, resistance)
- `src/modules/forzahorizon/process_watch.py` — psutil-based game process watcher for auto-exit
- `src/modules/dualsense/main.py` — HID writer: USB + Bluetooth, persistent mode when HidHide detected, CRC for BT reports
- `src/modules/dualsense/adaptive_trigger.py` — game-agnostic effect primitives (`off`, `rigid`, `vibrate`, `vibrate_zones`, `rigid_zones`). Run standalone: `python -m modules.dualsense.adaptive_trigger`
- `src/modules/dualsense/_hidraw.py` — Linux hidraw shim (PyPI hidapi uses libusb which can't claim the gamepad interface)
- `src/modules/dualsense/hidhide.py` — filesystem-only HidHide detection (no CLI calls)
- `src/modules/gui/` — CustomTkinter GUI with tabs: Controls, Profiles, Settings, System, Language, Logs
- `src/modules/tui/` — Textual TUI with same tab structure
- `src/lang/` — i18n: one module per language (`en`, `tr`, `zh`, `ja`, `ru`), auto-discovered via `NAME` + `STRINGS` dicts

### Data flow detail

1. `UDPListener.recv_latest()` drains queued packets, returns only the newest (never stale telemetry)
2. `forzahorizon.parse_packet()` unpacks the 324-byte Forza packet into a flat dict
3. `Controller.update(telemetry, settings)` runs L2 and R2 through priority chains — first non-empty effect wins
4. `loop.run()` diffs `(left, right)` against previous frame, only calls `ds.set()` on change
5. `DualSense.set()` builds the HID report, sets trigger bits in `valid_flag0` (0x04=R trigger, 0x08=L trigger), leaves rumble bytes untouched

### Settings / persistence

- `Settings` dataclass holds all defaults; `preferences.load()` overlays from `user_preferences.json`
- `GLOBAL_FIELDS` (udp_port, language, reconnect, etc.) persist across profiles; everything else is per-profile
- "Default" profile is reset to class defaults on every launch; named profiles are preserved
- Atomic file writes (`.tmp` → rename) to avoid corruption

## Conventions

- **KISS.** Don't abstract for one caller.
- All tunables go in `settings.py`, never inside module logic.
- **Globals stay global.** Add to `preferences.GLOBAL_FIELDS`; never copy into per-profile dicts.
- **Don't touch rumble bits.** HID writer only flips trigger bits in `valid_flag0`.
- **Always drain UDP** via `recv_latest()`; never react to stale packets.
- **State-change writes only.** The loop diffs `(left, right)` against `prev` and only calls `ds.set()` on change.
- No em dash (`—`) anywhere — in code, docs, or chat. Plain hyphens only.
- UTF-8 source files.
- Ruff: `line-length = 120`
- `IS_ZUV=true` env var is set by the zuv loader when running the bundle

## Common edits

| Want to... | Open this |
|---|---|
| Change a tunable / disable an effect | `src/modules/config/settings.py` |
| Change how an effect feels | `src/modules/dualsense/adaptive_trigger.py` (primitive) or `src/modules/forzahorizon/effects.py` (game logic) |
| Touch raw HID bytes | `src/modules/dualsense/main.py` |
| Add a telemetry field | `src/modules/forzahorizon/udp_listener.py` |
| Change CLI / startup wiring | `src/main.py` |
| Change persistence layout | `src/modules/config/preferences.py` |
| Edit the GUI | `src/modules/gui/` |
| Edit the TUI | `src/modules/tui/` |
| Add/translate a UI language | `src/lang/` (drop a `<code>.py` with `NAME` + `STRINGS`) |
| Change launcher behavior | `win_start.bat` / `linux_start.sh` |
| Change CI gating | `.github/workflows/release.yml` |

## HidHide

We do NOT call `HidHideCLI.exe`. `hidhide.is_detected()` is a pure filesystem probe. When detected, the I/O loop latches into **persistent mode**: keeps the HID handle open, ignores read/write errors, skips the watchdog, ignores `enable_reconnect`.

## CI

- Push to `dev` with `prerelease` in commit msg → rolling `v999.0.0` prerelease
- Push to `main` with `release vX.Y.Z` in commit msg → stable release
- Push tag `v*.*.*` → stable release
- `workflow_dispatch` → rolling prerelease