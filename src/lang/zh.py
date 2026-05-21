# -*- coding: utf-8 -*-
"""中文 (Chinese, Simplified) catalog. Keys are the English source strings."""

NAME = "中文"

STRINGS = {
    # --- chrome / tabs ---
    "Controls": "控制",
    "Profiles": "配置文件",
    "Settings": "设置",
    "System": "系统",
    "Language": "语言",
    "Logs": "日志",
    "Quit": "退出",
    "♥ Sponsor": "♥ 赞助",
    "Changelog": "更新日志",
    "connected": "已连接",
    "waiting": "等待中",
    "active": "当前",
    "(none)": "（无）",
    "Backend failed: {error}": "后端启动失败：{error}",
    "Profile: {name}": "配置文件：{name}",
    "Active: {name}": "当前：{name}",

    # --- settings tab sections ---
    "Pedal dead zones": "踏板死区",
    "Left trigger - Brake force": "左扳机 - 刹车力",
    "Left trigger - Static wall (optional)": "左扳机 - 静态防护墙（可选）",
    "Right trigger - Gas force": "右扳机 - 油门力",
    "ABS (anti-lock brake) rumble": "ABS（防抱死刹车）震动",
    "Redline (rev limiter) buzz": "红线（限速器）震动",
    "Wheelspin buzz": "车轮打滑震动",
    "Gear shift thump": "换挡冲击",

    # --- settings tab fields ---
    "Gas trigger dead zone": "油门扳机死区",
    "Brake trigger dead zone": "刹车扳机死区",
    "Resting stiffness": "静止阻力",
    "Hard-press stiffness": "重压阻力",
    "Stiffness curve shape": "阻力曲线形状",
    "Handbrake extra stiffness": "手刹额外阻力",
    "Wall position on the trigger": "扳机上的防护墙位置",
    "Wall hardness": "防护墙硬度",
    "Only when braking harder than": "仅在刹车力大于以下时",
    "Only when faster than (km/h)": "仅在车速大于以下时 (km/h)",
    "Wheel slip sensitivity": "车轮打滑灵敏度",
    "Tire grip sensitivity": "轮胎抓地灵敏度",
    "Rumble speed (Hz)": "震动速度 (Hz)",
    "Rumble strength": "震动强度",
    "Fire near redline at": "红线附近触发于",
    "Buzz speed (Hz)": "震动速度 (Hz)",
    "Buzz strength": "震动强度",
    "Buzz hold time (ms)": "震动保持时间 (ms)",
    "Thump speed (Hz)": "冲击速度 (Hz)",
    "Thump strength": "冲击强度",
    "Thump length (ms)": "冲击时长 (ms)",

    # --- settings tab buttons / hints ---
    "Reset to defaults": "恢复默认",
    "Click again to confirm reset": "再次点击以确认重置",
    "In Forza HUD: host 127.0.0.1 (try ::1 if it fails).":
        "在 Forza HUD 中: host 设为 127.0.0.1（若无效请尝试 ::1）。",
    "UDP port {port} is in use. Close the other listener or change the port in the System tab.":
        "UDP 端口 {port} 已被占用。请关闭其他监听程序，或在系统选项卡中更改端口。",

    # --- system tab sections / fields ---
    "Telemetry (applies on next launch)": "遥测（下次启动生效）",
    "Startup pulse": "启动脉冲",
    "Reconnect": "重新连接",
    "Game detection": "游戏检测",
    "UDP port": "UDP 端口",
    "Startup buzz strength": "启动震动强度",
    "Auto-reconnect when controller drops": "手柄断开时自动重连",
    "Reconnect check interval (s)": "重连检查间隔 (秒)",
    "Auto-exit when the game closes": "游戏关闭时自动退出",
    "Game-watch check interval (s)": "游戏监视间隔 (秒)",

    # --- system tab controller block ---
    "Controller": "手柄",
    "Lock to controller": "锁定到手柄",
    "Rescan": "重新扫描",
    "Auto (first found)": "自动（首个发现）",
    "attached now": "当前已连接",
    "(no serial - not selectable)": "（无序列号 - 无法选择）",

    # --- system tab updates block ---
    "Updates": "更新",
    "Check for updates at launch": "启动时检查更新",
    "When off, ZUV will not prompt for updates on startup. Toggle on and restart the app to check for a new release.":
        "关闭时，ZUV 不会在启动时提示更新。开启并重启应用以检查新版本。",
    "ZUV not found: this build is not running inside a ZUV bundle (ZUV_CACHE_ROOT env var is missing), so the update toggle has nothing to control. Run the bundled .zuv.py to manage updates.":
        "未找到 ZUV：此版本未在 ZUV 包内运行（缺少 ZUV_CACHE_ROOT 环境变量），因此更新开关无可控制对象。请运行打包的 .zuv.py 来管理更新。",

    # --- profiles tab ---
    "Load": "加载",
    "Rename": "重命名",
    "Delete": "删除",
    "Save": "保存",
    "New profile name": "新配置文件名",
    "File: {path}": "文件：{path}",
    "Note: the [b]Default[/] profile is reset to built-in values every time the app launches so new features and tuning come through. System settings (System tab) are preserved. To keep your own tuning across launches, save it as a named profile here.":
        "注意：[b]Default[/] 配置文件会在每次启动时重置为内置值，以便引入新功能和调校。系统设置（系统选项卡）会被保留。要在多次启动间保留您自己的调校，请在此另存为命名配置文件。",

    # --- logs tab ---
    "level": "级别",
    "pause": "暂停",
    "resume": "继续",
    "clear": "清除",

    # --- system tab DSX block ---
    "DSX output": "DSX 输出",
    "Force DSX output (auto-detected when DSX is running)": "强制 DSX 输出（DSX 运行时自动检测）",
    "DSX is used automatically when DSX.exe is detected. Enable this to force DSX even when not detected.":
        "检测到 DSX.exe 时自动使用 DSX。启用此项可在未检测到时强制使用 DSX。",
    "Auto-detect DSX port": "自动检测 DSX 端口",
    "Reads DSX_UDP_PortNumber.txt from %LOCALAPPDATA%\\DSX.":
        "从 %LOCALAPPDATA%\\DSX 读取 DSX_UDP_PortNumber.txt。",
    "DSX host": "DSX 主机",
    "DSX port": "DSX 端口",
    "Controller index": "手柄编号",
    "DSX: checking...": "DSX：检测中…",
    "DSX: running": "DSX：运行中",
    "DSX: not detected": "DSX：未检测到",
    "Refresh": "刷新",
    "[bold red]DSX open failed — HID fallback[/]": "[bold red]DSX 启动失败 — 已回退至 HID[/]",

    # --- language tab ---
    "Pick a language, then restart the app to apply it.":
        "选择一种语言，然后重启应用以应用更改。",
    "Restart the app to apply the new language.":
        "重启应用以应用新语言。",
}
