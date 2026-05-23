<p align="right">
  <strong>English</strong> •
  <a href="docs/ReadmeTR.md">Türkçe</a> •
  <a href="docs/ReadmeJA.md">日本語</a> •
  <a href="docs/ReadmeZH.md">简体中文</a>
</p>

<div align="center">
  <h1>🏎️ Forza Horizon - DualSense Adaptive Triggers</h1>
  <p><strong>Real trigger feedback for Forza Horizon on PC.</strong></p>
  <p><em>Feel the brakes. Feel the engine. No setup juggling.</em></p>
</div>

> My Steam profile: <https://steamcommunity.com/id/teccno/>
> 
> For CS:GO item Sponsorship :D : <https://steamcommunity.com/tradeoffer/new/?partner=291638630&token=Xyg4vITU>

<div align="center">
  <a href="https://www.youtube.com/watch?v=-3Cp0PfL52Y">
    <img src="docs/img/tuiyoutube.png" alt="Forza Horizon DualSense Adaptive Trigger Mod" style="width:100%;">
  </a>
</div>

> 💛 Huge thanks to **[Jared (jmac122)](https://github.com/jmac122)** for sponsoring this project by gifting me Forza Horizon 6.

---

## 📜 Contents
1. [What it does](#-what-it-does)
2. [Install](#-install)
3. [In-game setup](#-in-game-setup)
4. [Enable Steam Haptics](#-enable-steam-haptics)
5. [Run it](#-run-it)
6. [Auto-launch with Steam](#-auto-launch-with-steam)
7. [Tuning the feel](#-tuning-the-feel)
8. [Troubleshooting](#-troubleshooting)
9. [Credits](#-credits)



---

## 💡 What it does

Forza Horizon sends car telemetry over UDP, but Steam Input doesn't use the DualSense's **adaptive triggers**. This tiny app fills the gap:

- **Left trigger (brake)** — pushes back harder the more you press. Buzzes like ABS when tires slip. Extra resistance when handbraking.
- **Right trigger (throttle)** — soft progressive resistance. Thumps on gear shifts. Buzzes at the rev limiter.

### How it talks to your controller without fighting Steam

```
┌──────────────────┐    UDP 5300     ┌──────────────────┐    HID write    ┌─────────────┐
│  Forza Horizon   │ ──────────────► │  This app        │ ──────────────► │  DualSense  │
│  (Data Out)      │  telemetry      │  (trigger bits   │  triggers only  │  controller │
└──────────────────┘  324 bytes      │   only)          │                 └─────────────┘
                                     └──────────────────┘                        ▲
                                                                                 │
                                     ┌──────────────────┐    HID write           │
                                     │  Steam Input     │ ──────────────────────►│
                                     │  (rumble bits)   │  rumble + buttons      │
                                     └──────────────────┘
```

Both the app and Steam write to the same controller — but they touch **different bytes**:

- Steam owns the **rumble motors** and button mapping.
- This app only flips the **adaptive trigger** bits (`valid_flag0` bits `0x04` and `0x08`).
- The HID device is opened in **non-blocking mode**, so writes fire immediately instead of waiting on the controller. Nothing gets queued, nothing blocks Steam.

That's why you can run both at the same time and neither one breaks the other.

---

## 🛠️ Install

**You need:** Windows 10/11 or Linux, and a DualSense controller (USB or Bluetooth).

1. Go to the [latest release](https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python/releases/latest).
2. Download **`win_start.bat`** (Windows) or **`linux_start.sh`** (Linux).
3. Put it in any empty folder.
4. **Important:** We highly recommend installing **`uv`** manually first. Open PowerShell and run this command:
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
   - If you skip this, `win_start.bat` will try to install `uv` automatically. However, Windows might block this auto-install with an "Execution Policy" error in PowerShell.
   - **If you get the Execution Policy error:** Hold **Shift + Right-Click** in the folder, click **"Open PowerShell window here"**, paste `Set-ExecutionPolicy RemoteSigned -scope CurrentUser` and hit Enter, then type `Y` and Enter.
5. Double-click `win_start.bat` (or `linux_start.sh`).

The launcher handles downloading the app, preparing the environment, and running it. Next time you run it, it will also check for updates.

> [!NOTE]
> A standalone **Windows `.exe`** is also attached to each release as an experimental option. The **recommended** way to run the app is still **`win_start.bat`** — it self-updates and works the same across every Windows version.

> **Linux extras:** install `libhidapi` (`sudo apt install libhidapi-hidraw0` / `sudo pacman -S hidapi` / `sudo dnf install hidapi`) and the udev rule from `app/packaging/linux/70-dualsense.rules`. Then unplug/replug the controller once.

### 🎮 Playing with SISR (Xbox App / Windows Store users)

If you are playing the game via the Xbox App or Microsoft Store, you will need a tool that makes the game recognize your controller as an Xbox controller. One option is **[SISR (Steam Input System Redirector)](https://github.com/Alia5/SISR)** — it redirects Steam Input to the system level and emulates a real Xbox controller, so it works even with Windows Store apps and anti-cheat-protected games.

Because SISR routes the controller through **Steam Input**, Steam can grab the physical DualSense exclusively and prevent this app from connecting. To avoid this, **you must start the programs in this exact order**:

1. **First, launch THIS APP** (`win_start.bat`) and wait for the short pulse on the triggers.
2. **Second, launch SISR** (and Steam).
3. **Finally, launch Forza Horizon.**

*(Note: If your controller disconnects while playing, close SISR, restart this app, then open SISR again. For SISR setup and emulation options, see the [SISR README](https://github.com/Alia5/SISR).)*

<details>
<summary>Manual install (for developers)</summary>

```bash
git clone https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python
cd Forza-Horizon-DualSense-Python/src
uv sync
uv run main.py
```

Need `uv`? `pip install uv` or [astral.sh/uv](https://astral.sh/uv/).
</details>

---

## 🎯 In-game setup

In Forza Horizon, open **Settings → HUD and Gameplay** and scroll to the bottom:

| Setting | Value |
|---------|-------|
| Data Out | **ON** |
| Data Out IP Address | **127.0.0.1** |
| Data Out IP Port | **5300** |

> [!NOTE]
> In some versions of Forza, entering `127.0.0.1` as the IP address may not work. If the application doesn't receive telemetry, try entering `::1` (IPv6 loopback) instead.

<p align="center">
  <img src="docs/img/en.png" alt="English Settings" width="48%" style="border-radius: 8px;">
  &nbsp;
  <img src="docs/img/tr.png" alt="Turkish Settings" width="48%" style="border-radius: 8px;">
</p>

---

## 🔊 Enable Steam Haptics

**Steam** can vibrate the left and right rumble motors on your DualSense controller. To enable them:

### In Steam:
1. Right-click **Forza Horizon** in your library → **Properties**.
2. Go to **Controller → Additional Settings**.
3. Make sure **DualSense vibration** is turned **ON**.

### In-game (Forza Horizon):
1. Open **Settings → Advanced Controls**.
2. Find the **Vibration** option and enable it.

### DualSense software:
For best results, install the official **PlayStation® Accessories** software:
- Download: [PlayStation® Accessories](https://fwupdater.dl.playstation.net/fwupdater/PlayStationAccessoriesInstaller.exe)

This ensures your DualSense firmware is up to date for windows.

> ℹ️ **About Adaptive Triggers:** Steam doesn't support DualSense adaptive triggers for this game. That's what **this app** does — it adds realistic trigger feedback (brake resistance, engine feedback, ABS pulses, gear thumps, rev limiter buzz) on top of the rumble that Steam provides.

---

## ▶️ Run it

Double-click **`win_start.bat`** (Windows) or **`linux_start.sh`** (Linux).

You'll feel a short pulse on both triggers — that means it's working. Now launch Forza Horizon and drive.

> Start the launcher **before** Forza Horizon. If you use HidHide, allowlist `python.exe`.

---

## 🎮 Auto-launch with Steam

Want the triggers to turn on automatically when you press **Play**? Tell Steam to run the launcher first.
> ⚠️ **Warning:** Sometimes auto-launching this way can cause issues with the application. For the most stable experience, it is recommended to launch the app manually by double-clicking the script.

1. In Steam, right-click **Forza Horizon** → **Properties**.
2. Open the **General** tab and find **Launch Options**.
3. Choose one of the following commands based on your preference (change the path to where your `win_start.bat` actually is):

   * **Option A: Keeping Steam Overlay & Playtime Tracking (Recommended)**
     This wraps the script in `cmd.exe /c` so Steam can properly monitor the process, keeping your **Steam Overlay (Shift+Tab)** and **Playtime Tracking** fully functional while automatically closing the console window afterwards:
     ```text
     "C:\Windows\System32\cmd.exe" /c ""C:\Your\Path\To\Forza-Horizon-DualSense-Python\win_start.bat" %command%"
     ```

   * **Option B: Simpler Method**
     A direct way to launch, though the Steam Overlay and playtime tracking may stop working:
     ```text
     "C:\Your\Path\To\Forza-Horizon-DualSense-Python\win_start.bat" %command%
     ```

That's it. Press **Play** - the launcher runs, then the game opens.

![Steam launch options](docs/img/steaming.png)

<details>
<summary>Advanced — run the Python script directly (no BAT file)</summary>

If you cloned the repo and use `uv`, paste this into **Launch Options** instead:

```text
cmd /c "start /MIN /D C:\Your\Path\To\Forza-Horizon-DualSense-Python\src uv run main.py" && %command%
```
</details>

---

## 🎚️ Tuning the feel

Every effect (brake force, ABS buzz, gear thump, rev limiter, etc.) can be tweaked or turned off from the **Settings page in the app** — no file editing needed. Changes apply on next launch.

> ⚠️ The rev limiter fires based on `rpm / max_rpm`, not a fixed RPM. Different cars hit redline at different ratios, so it may need per-car tweaking.

---

## 🩺 Troubleshooting

| Symptom | Fix |
|---------|-----|
| `DualSense gamepad interface not found` | Controller not connected, or HidHide is hiding it — allowlist `python.exe`. |
| `No UDP packets yet` | Forza's Data Out is off, IP/port is wrong, Windows Firewall is blocking, or try changing the IP from `127.0.0.1` to `::1`. |
| Windows Defender / SmartScreen blocks `win_start.bat` | 1. On the blue "Windows protected your PC" screen, click **"More info"**.<br>2. Click the **"Run anyway"** button that appears at the bottom. (The script only downloads required dependencies.) |
| Triggers feel weak | Raise `brake_max_force` / `throttle_max_force`, or lower the matching `curve`. |
| Triggers feel like a brick wall | Lower `brake_max_force` / `throttle_max_force`, or raise the matching `curve`. |
| Triggers feel stiff at a light press | Lower the baseline force, or raise the `curve`. |
| No vibration on gear shift | Car must be moving faster than 3 km/h and changing between valid gears. |
| Console window is blank after the startup pulse | Run from a terminal with `cd src && uv run main.py --headless` to skip the TUI. |

---

## 📁 Project layout

```
src/
├── main.py                          # Entry point
└── modules/
    ├── settings.py                  # 👈 the file you edit
    ├── dualsense/
    │   ├── main.py                              # HID layer
    │   └── adaptive_trigger.py                 # generic effect primitives
    └── forzahorizon/
        ├── udp_listener.py                     # UDP parser
        └── effects.py                          # Forza-aware Controller + animations
```

---

## 🙏 Credits

Built by **[HamzaYslmn](https://github.com/HamzaYslmn)**.

### 💛 Sponsors

- **[Jared (jmac122)](https://github.com/jmac122)** — gifted me Forza Horizon 6 so this project could keep moving forward. Thank you, Jared!
- **[BeaudinSan](https://github.com/BeaudinSan)** — thank you for your incredibly generous support! It truly means a lot to me. 
- **[McLarenF1God](https://github.com/McLarenF1God)** — thank you for Forza Horizon 6 DLC's
- **[PlusMinusZer0](https://github.com/PlusMinusZer0)** — thank you for your Pudding!
- **[dotcom](https://github.com/a0938670973-dotcom)** — thank you for your Cake!
- **[wallbangz](https://github.com/wallbangz)** — thank you for your Cake!
- **[BambinoPinguino](https://github.com/BambinoPinguino)** — thank you for your Tea!
- **[Ereldun](https://steamcommunity.com/)** — thank you for your Coffee!
- **[Clevens克林](https://steamcommunity.com/)** — thank you for your Candy!

A heartfelt thank you as well to the anonymous sponsors who quietly supported this project, and to everyone whose appreciation, kind words, and social media shares helped keep me motivated throughout the journey.

---
*Built for an immersive racing experience*
