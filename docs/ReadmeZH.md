<p align="right">
  <a href="../README.md">English</a> •
  <a href="ReadmeTR.md">Türkçe</a> •
  <a href="ReadmeJA.md">日本語</a> •
  <strong>简体中文</strong>
</p>

<div align="center">
  <h1>🏎️ Forza Horizon - DualSense Adaptive Triggers</h1>
  <p><strong>PC 端地平线（Forza Horizon）手柄真实扳机反馈。</strong></p>
  <p><em>感受刹车。感受引擎。免去繁琐设置。</em></p>
</div>

> 我的 Steam 个人主页: <https://steamcommunity.com/id/teccno/>
> 
> 用于赞助的 CS:GO 交易链接 :D : <https://steamcommunity.com/tradeoffer/new/?partner=291638630&token=Xyg4vITU>

<div align="center">
  <a href="https://www.youtube.com/watch?v=-3Cp0PfL52Y">
    <img src="img/tuiyoutube.png" alt="Forza Horizon DualSense Adaptive Trigger Mod" style="width:100%;">
  </a>
</div>

> 💛 非常感谢 **[Jared (jmac122)](https://github.com/jmac122)** 送给我《极限竞速：地平线 6》来赞助支持本项目，让它能够继续发展。

---

## 📜 目录
1. [功能简介](#-功能简介)
2. [安装步骤](#-安装步骤)
3. [游戏内设置](#-游戏内设置)
4. [启用 Steam 触感反馈](#-启用-steam-触感反馈)
5. [启动运行](#-启动运行)
6. [随 Steam 自动启动](#-随-steam-自动启动)
7. [调校反馈手感](#-调校反馈手感)
8. [故障排查](#-故障排查)
9. [赞助与致谢](#-赞助与致谢)

---

## 💡 功能简介

《极限竞速：地平线》通过 UDP 发送车辆遥测数据，但 Steam 输入默认无法使用 DualSense 的**自适应扳机**。这个小程序弥补了这一空缺：

- **左扳机（刹车）** - 踩得越深，阻力越大。当轮胎打滑时，会产生类似 ABS 介入的防抱死震动。拉起手刹时，会有额外的阻力加成。
- **右扳机（油门）** - 柔和的渐进阻力。换挡时会有明显的换挡冲击。转速达到红线区时会有震动。

### 它是如何在不与 Steam 冲突的情况下与手柄通信的

```
┌──────────────────┐    UDP 5300     ┌──────────────────┐    HID 写入     ┌─────────────┐
│  Forza Horizon   │ ──────────────► │  本程序          │ ──────────────► │  DualSense  │
│  (数据输出)      │ 遥测数据 324字节 │  (仅控制扳机字节)│  (仅修改自适应  │   手柄      │
└──────────────────┘                 └──────────────────┘   扳机效果)     └─────────────┘
                                                                                 ▲
                                                                                 │
                                     ┌──────────────────┐    HID 写入            │
                                     │  Steam Input     │ ───────────────────────►│
                                     │  (控制常规震动)  │  (常规震动 + 按键输入)  │
                                     └──────────────────┘
```

本程序和 Steam 同时对一个手柄进行写入 - 但它们操作的是**不同的字节**：

- Steam 掌控的是手柄的**基础震动马达**和按键映射。
- 本程序仅修改与**自适应扳机**相关的字节（`valid_flag0` 内的 `0x04` 和 `0x08` 位）。
- HID 设备是以**非阻塞模式（non-blocking mode）**打开的，所以写入指令会立即发送，而不会等待手柄响应。不会产生队列积压，也不会阻塞 Steam 的输入。

这就是为什么你可以同时运行这两个程序而互不干扰。

---

## 🛠️ 安装步骤

**运行要求:** Windows 10/11 或 Linux，以及 DualSense 手柄（USB 或蓝牙连接）。

1. 前往 [最新发布版本 (latest release)](https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python/releases/latest)。
2. 下载 **`win_start.bat`** (Windows) 或 **`linux_start.sh`** (Linux)。
3. 将下载的文件放到任意一个空白文件夹中。
4. **重要:** 我们强烈建议您先手动安装 **`uv`** 环境。打开 PowerShell 并运行以下命令：
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
   - 如果您跳过此步，`win_start.bat` 在启动时会尝试自动下载安装 `uv`。但 Windows 的执行策略（Execution Policy）可能会在 PowerShell 中拦截并导致自动安装失败。
   - **如果遇到执行策略（Execution Policy）报错:** 在所在的文件夹中按住 **Shift + 右键**，点击 **“在此处打开 PowerShell 窗口”**，粘贴 `Set-ExecutionPolicy RemoteSigned -scope CurrentUser` 并回车，然后输入 `Y` 回车确认。
5. 双击运行 `win_start.bat` (或 `linux_start.sh`)。

启动器会自动完成应用下载、环境配置以及程序启动。下次运行它时，还会自动检查更新。

> [!NOTE]
> 每个版本还附带一个独立的 **Windows `.exe`** 作为实验性选项。**推荐**的运行方式仍然是 **`win_start.bat`** —— 它会自动更新，并在所有 Windows 版本上以相同方式工作。

> **Linux 额外说明:** 安装 `libhidapi` 依赖（`sudo apt install libhidapi-hidraw0` / `sudo pacman -S hidapi` / `sudo dnf install hidapi`）并从 `app/packaging/linux/70-dualsense.rules` 添加 udev 规则。然后将手柄断开并重新连接一次。

### 🎮 使用 SISR 玩游戏（Xbox App / 微软商店版用户）

如果您是在微软商店（Microsoft Store）或 Xbox App 上运行游戏，您将需要一个工具来让游戏把您的手柄识别为 Xbox 手柄。其中一个选择是 **[SISR（Steam Input System Redirector）](https://github.com/Alia5/SISR)** —— 它将 Steam Input 重定向到系统层级并模拟一个真实的 Xbox 手柄，因此即使在微软商店应用和带反作弊保护的游戏中也能正常工作。

因为 SISR 通过 **Steam Input** 转发手柄，Steam 可能会独占物理 DualSense 手柄，导致本程序无法连接。为了避免这个问题，**您必须按照以下严格的顺序启动程序**：

1. **首先启动本程序** (`win_start.bat`)，等待扳机发生一次简短的脉冲震动。
2. **第二步，启动 SISR（以及 Steam）。**
3. **最后，启动极限竞速：地平线游戏。**

*(注：如果在玩游戏时手柄断开连接，请先关闭 SISR，重启本程序，然后再打开 SISR。有关 SISR 的安装与模拟选项，请参阅 [SISR README](https://github.com/Alia5/SISR)。)*

<details>
<summary>手动安装（适合开发者）</summary>

```bash
git clone https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python
cd Forza-Horizon-DualSense-Python/src
uv sync
uv run main.py
```

需要安装 `uv`？ 使用 `pip install uv` 或访问 [astral.sh/uv](https://astral.sh/uv/)。
</details>

---

## 🎯 游戏内设置

在《极限竞速：地平线》中，打开 **设置 → HUD 与游戏玩法**，滚动到最下方：

| 设置项 | 数值 |
|---------|-------|
| 数据输出 (Data Out) | **开启 (ON)** |
| 数据输出 IP 地址 (Data Out IP Address) | **127.0.0.1** |
| 数据输出端口 (Data Out IP Port) | **5300** |

> [!NOTE]
> 在某些版本的地平线游戏中，将 IP 地址填写为 `127.0.0.1` 可能会失效。如果程序没有收到任何遥测包，请尝试改填为 `::1`（IPv6 环回地址）。

<p align="center">
  <img src="img/en.png" alt="英文设置" width="48%" style="border-radius: 8px;">
  &nbsp;
  <img src="img/tr.png" alt="土耳其文设置" width="48%" style="border-radius: 8px;">
</p>

---

## 🔊 启用 Steam 触感反馈

**Steam** 可以驱动 DualSense 手柄上的左右常规震动马达。请按照以下步骤开启：

### Steam 端设置:
1. 在 Steam 库中右键点击 **极限竞速：地平线** → **属性**。
2. 转到 **控制器 → 额外设置**。
3. 确保 **DualSense 震动** 选项设置为 **开启**。

### 游戏内设置 (极限竞速：地平线):
1. 打开 **设置 → 高级控制**。
2. 找到 **震动** 选项并将其启用。

### 手柄驱动软件:
为了获得最佳效果，建议安装官方的 **PlayStation® Accessories** 固件更新软件：
- 下载地址: [PlayStation® Accessories](https://fwupdater.dl.playstation.net/fwupdater/PlayStationAccessoriesInstaller.exe)

这可以确保您的 DualSense 固件保持最新状态。

> ℹ️ **关于自适应扳机:** 正常情况下，Steam 并不支持此游戏在 DualSense 手柄上的自适应扳机效果。**本程序**的全部意义就在于——在 Steam 原生的震动效果基础之上，叠加还原真实的扳机反馈（刹车阻力、引擎颤动、ABS 脉动、换挡冲击、红线转速抖动）。

---

## ▶️ 启动运行

双击 **`win_start.bat`** (Windows) 或 **`linux_start.sh`** (Linux)。

你会感到手柄扳机产生了一次简短的脉冲震动，这代表一切运行正常。此时可以开启游戏上路了。

> 请务必在运行极限竞速游戏**之前**运行启动器。如果您使用了 HidHide，请确保将 `python.exe` 加入白名单。

---

## 🎮 随 Steam 自动启动

想在 Steam 点击 **开始游戏** 时，自适应扳机也能自动开启？你可以把启动器的路径写入 Steam 启动选项中。
> ⚠️ **警告:** 部分系统环境下这种启动方式可能会导致程序连接出错。为了获得最稳定的体验，我们依然强烈建议您直接双击运行脚本来手动启动程序。

1. 在 Steam 中，右键点击 **极限竞速：地平线** → **属性**。
2. 打开 **通用** 标签页，并找到 **启动选项**。
3. 根据个人喜好，填入以下命令之一（记得将路径修改为您的 `win_start.bat` 的实际位置）：

   * **方式 A：保留 Steam 界面叠加层和游戏时间统计 (推荐)**
     这行命令通过 `cmd.exe /c` 包装脚本，让 Steam 能正常监视游戏进程，确保你的 **Steam 界面 (Shift+Tab)** 以及 **游戏时间统计** 功能正常可用，并且命令行窗口在运行后会自动关闭：
     ```text
     "C:\Windows\System32\cmd.exe" /c ""C:\您的路径\Forza-Horizon-DualSense-Python\win_start.bat" %command%"
     ```

   * **方式 B：极简命令方式**
     直接拉起脚本，但可能导致 Steam 界面叠加层和游戏时间统计失效：
     ```text
     "C:\您的路径\Forza-Horizon-DualSense-Python\win_start.bat" %command%
     ```

大功告成。点击 **开始游戏** 时，启动器就会首先拉起，随后运行游戏。

![Steam 启动选项](img/steaming.png)

<details>
<summary>高级 - 直接运行 Python 脚本（不使用 BAT 文件）</summary>

如果您克隆了本仓库并且正在使用 `uv` 运行，可以把以下命令复制到 **启动选项** 中：

```text
cmd /c "start /MIN /D C:\您的路径\Forza-Horizon-DualSense-Python\src uv run main.py" && %command%
```
</details>

---

## 🎚️ 调校反馈手感

所有的效果（刹车力度、ABS 震动、换挡冲击、红线震动等）都可以在**程序的设置（Settings）页面**中进行调校或关闭，不需要手动编辑任何文件。修改将在下次启动程序时生效。

> ⚠️ 红线限速器效果是根据 `rpm / max_rpm` 比例触发的，而不是固定的 RPM。不同车型的红线比例各不相同，因此可能需要根据车型做出细微调校。

---

## 🩺 故障排查

| 故障现象 | 解决方法 |
|---------|---------|
| `DualSense gamepad interface not found` | 手柄没有连接，或者 HidHide 屏蔽了手柄 - 请把 `python.exe` 添加到白名单中。 |
| `No UDP packets yet` | 地平线游戏里的“数据输出（Data Out）”选项没有开启，IP 地址或端口填写错误，或者 Windows 防火墙进行了拦截。也可以尝试把数据输出 IP 从 `127.0.0.1` 更改为 `::1`。 |
| Windows Defender / SmartScreen 拦截了 `win_start.bat` | 1. 在蓝色的“Windows 已保护你的电脑”警告弹窗中，点击 **“更多信息”**。<br>2. 点击右下角新出现的 **“仍要运行”** 按钮即可（脚本仅下载所需的依赖库，安全无毒）。 |
| 扳机感觉太软（阻力太小） | 调大 `brake_max_force` / `throttle_max_force`，或者调小对应的阻力曲线 `curve` 数值。 |
| 扳机感觉像一堵硬墙（阻力太大） | 调小 `brake_max_force` / `throttle_max_force`，或者调大对应的阻力曲线 `curve` 数值。 |
| 轻按扳机时就感觉非常僵硬 | 调小基础力度 `baseline_force`，或者调大阻力曲线 `curve` 数值。 |
| 换挡时没有任何震动反馈 | 车辆速度必须高于 3 km/h，并且处于有效挡位之间的切换状态。 |
| 在启动脉冲过后面版窗口处于空白无响应状态 | 在终端中使用 `cd src && uv run main.py --headless` 运行以跳过 TUI 界面，改用纯控制台日志输出。 |

---

## 📁 项目结构

```
src/
├── main.py                          # 入口文件
└── modules/
    ├── settings.py                  # 👈 你需要调校参数的文件
    ├── dualsense/
    │   ├── main.py                              # HID 设备交互层
    │   └── adaptive_trigger.py                 # 通用扳机效果原语
    └── forzahorizon/
        ├── udp_listener.py                     # UDP 遥测数据解析
        └── effects.py                          # Forza 专属 Controller 与动画
```

---

## 🙏 赞助与致谢

由 **[HamzaYslmn](https://github.com/HamzaYslmn)** 开发完成。

### 💛 赞助者

- **[Jared (jmac122)](https://github.com/jmac122)** - 送给我《极限竞速：地平线 6》以支持这个项目能够继续维护下去，非常感谢你，Jared!
- **[BeaudinSan](https://github.com/BeaudinSan)** - 感谢您极为慷慨的赞助支持！这对我有非凡的意义。
- **[McLarenF1God](https://github.com/McLarenF1God)** - 感谢赞助《极限竞速：地平线 6》的 DLC！
- **[PlusMinusZer0](https://github.com/PlusMinusZer0)** - 感谢送给我的布丁！
- **[dotcom](https://github.com/a0938670973-dotcom)** - 感谢送给我的蛋糕！
- **[wallbangz](https://github.com/wallbangz)** - 感谢送给我的蛋糕！
- **[BambinoPinguino](https://github.com/BambinoPinguino)** - 感谢送给我的茶！
- **[Ereldun](https://steamcommunity.com/)** - 感谢送给我的咖啡！
- **[Clevens克林](https://steamcommunity.com/)** - 感谢送给我的糖果！

---
*为了更具沉浸感的赛车游戏体验而打造*
