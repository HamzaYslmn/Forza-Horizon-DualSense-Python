# AGENTS.md

Short tour. The full module-by-module reference is in the code; this is just a map.

## What it is

Small Python service. Reads Forza Horizon's UDP telemetry (5300) and drives
**DualSense adaptive triggers** over raw HID, while leaving rumble bytes alone
so Steam Input still handles rumble.

## Stack

- Python `>=3.13`, `uv` for deps.
- Deps: `hidapi`, `textual`, `psutil`.
- Distributed as a single self-contained file (`fhds.zuv.py`) via [`zuv`](https://github.com/HamzaYslmn/zuv).
- Windows + Linux. No tests.

## Layout

```
src/
  main.py                    # entry: IS_ZUV check, args, TUI/headless boot
  pyproject.toml             # version, deps, [tool.zuv] entry+volume
  modules/
    settings.py              # @dataclass Settings - ALL tunables live here
    preferences.py           # JSON persistence (globals + active profile)
    profiles.py              # named profile CRUD
    loop.py                  # per-packet driver
    udplistener/main.py      # UDP socket + 324-byte FH packet parser
    dualsense/
      main.py                # HID writer (USB+BT), persistent mode
      triggers.py            # effect primitives + TriggerAnimation
      hidhide.py             # filesystem-only HidHide detection
    tui/                     # Textual app (controls/settings/profiles/logs)
    emulation/               # optional fake telemetry for offline dev
    exit_detection/          # watches game proc, closes when it exits
win_start.bat / linux_start.sh   # launchers (auto-download bundle + run uv)
app/fhds.zuv.py              # the actual bundle users run
.github/workflows/release.yml    # CI: build bundle, publish release
```

## Data flow (one frame)

```
FH UDP 5300 -> parse_packet -> TriggerAnimation.update -> (left, right)
                                                              |
                              DualSense.set (state-change only)
                                                              v
                                                  HID write (trigger bytes only,
                                                   rumble bytes untouched)
```

Trigger command = `(mode, p1, p2)`:
- `M_OFF (0x05)` free, `M_RIGID (0x01)` constant force, `M_PULSE (0x06)` vibration.

## Run

### Dev (no bundle)
```powershell
cd src
uv sync
$env:FHDS_DEV = "1"      # suppress the "old standalone" startup prompt
uv run main.py
```

### Build the bundle locally (same as CI)

One-liner:
```powershell
uvx zuv build src -o app/fhds.zuv.py --update-repo HamzaYslmn/Forza-Horizon-DualSense-Python
```

Drop `--update-repo` if you don't want the bundle to self-update from GitHub
on next launch (useful while iterating locally).

Bump the version first by editing `version = "X.Y.Z"` in `src/pyproject.toml`.

### Run the bundle
```powershell
.\win_start.bat
```
Launcher auto-downloads `app/fhds.zuv.py` if missing, installs `uv` if missing,
then `uv run`s the bundle.

### In-game (once)
Forza Horizon -> **Settings -> HUD and Gameplay -> Data Out: ON**, IP `127.0.0.1`,
Port `5300`.

## CI gating

`.github/workflows/release.yml`:
- Push to `dev` with `prerelease` in commit msg -> rolling `v999.0.0` prerelease.
- Push to `main` with `release vX.Y.Z` in commit msg -> stable `vX.Y.Z`.
- Push tag `v*.*.*` -> stable release.
- `workflow_dispatch` -> rolling prerelease.

## Env vars

- `IS_ZUV=true` - set automatically by the zuv loader when running the bundle.
  `main.py` warns + blocks on `[y/N]` if missing (means user is on old standalone flow).
- `FHDS_DEV=1` - suppresses that warning during dev.

## Conventions

- **KISS.** Don't abstract for one caller.
- All tunables go in `settings.py`, never inside module logic.
- **Globals stay global.** Add to `preferences.GLOBAL_FIELDS`; never copy into per-profile dicts.
- **Don't touch rumble bits.** HID writer only flips trigger bits in `valid_flag0`.
- **Always drain UDP** via `recv_latest()`; never react to stale packets.
- **State-change writes only.** The loop diffs `(left, right)` against `prev` and only calls `ds.set(...)` on change.
- No em dash (`-`) anywhere - in code, docs, or chat. Plain hyphens only.
- UTF-8 source files.

## HidHide

We do NOT call `HidHideCLI.exe`. `hidhide.is_detected()` is a pure filesystem
probe. When detected, the I/O loop latches into **persistent mode** on the
first successful connect: keeps the HID handle open, ignores read/write
errors, skips the watchdog, ignores the `enable_reconnect` setting. This way
HidHide cloaking the device mid-session doesn't tear our handle down.

## Common edits

| Want to... | Open this |
|---|---|
| Change a tunable / disable an effect | `src/modules/settings.py` |
| Change how an effect feels | `src/modules/dualsense/triggers.py` |
| Touch raw HID bytes | `src/modules/dualsense/main.py` |
| Add a telemetry field | `src/modules/udplistener/main.py` |
| Change CLI / startup wiring | `src/main.py` |
| Change persistence layout | `src/modules/preferences.py` |
| Edit the TUI | `src/modules/tui/` |
| Change launcher behavior | `win_start.bat` / `linux_start.sh` |
| Change CI gating | `.github/workflows/release.yml` |
