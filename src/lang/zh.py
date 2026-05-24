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

    # --- controls tab (per-trigger effect switches) ---
    "Shift thump": "换挡冲击",
    "ABS rumble": "ABS 震动",
    "Static brake wall": "刹车静态防护墙",
    "Brake stiffness": "刹车阻力",
    "Handbrake stiffness bonus": "手刹额外阻力",
    "Redline buzz": "红线震动",
    "Wheelspin buzz": "车轮打滑震动",
    "Idle buzz": "怠速震动",
    "Throttle stiffness": "油门阻力",

    # --- settings tab sections ---
    "Pedal dead zones": "踏板死区",
    "Left trigger - Brake force": "左扳机 - 刹车力",
    "Left trigger - Static wall (optional)": "左扳机 - 静态防护墙（可选）",
    "Right trigger - Gas force": "右扳机 - 油门力",
    "ABS (anti-lock brake) rumble": "ABS（防抱死刹车）震动",
    "Redline (rev limiter) buzz": "红线（转速限制器）震动",
    "Wheelspin buzz": "车轮打滑震动",
    "Idle buzz": "怠速震动",
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
    "Fire near redline at": "接近红线时触发",
    "Buzz speed (Hz)": "震动速度 (Hz)",
    "Buzz strength": "震动强度",
    "Buzz hold time (ms)": "震动保持时间 (ms)",
    "Idle strength": "怠速强度",
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
    "Startup pulse": "启动震动",
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

    # --- language tab ---
    "Pick a language, then restart the app to apply it.":
        "选择一种语言，然后重启应用以应用更改。",
    "Restart the app to apply the new language.":
        "重启应用以应用新语言。",
    "Speed-based throttle": "基于速度的油门",
    "Extra force at standstill": "静止时额外力度",
    "Fade-out speed (km/h)": "衰减速度 (km/h)",
    "Extra resistance at low speed for precise control, lighter at high speed.":
        "低速时增加阻力以实现精确控制，高速时更轻。",
    "0 = off. Flat resistance added at 0 km/h, fading to normal.":
        "0 = 关闭。在0 km/h时增加平坦阻力，逐渐衰减至正常。",
    "Speed where boost fully fades. Default 80.":
        "增益完全衰减的速度。默认80。",
    "Surface brake resistance": "路面刹车阻力",
    "Tarmac multiplier": "柏油路倍率",
    "Dirt multiplier": "泥土路倍率",
    "Gravel multiplier": "碎石路倍率",
    "Softer brake on loose surfaces, firmer on tarmac.":
        "松散路面刹车更软，柏油路更硬。",
    "1.0 = unchanged. Scales final resistance force.":
        "1.0 = 不变。缩放最终阻力力度。",
    "Lower = softer brake on dirt. Default 0.5.":
        "越低 = 泥土路刹车越软。默认0.5。",
    "Lower = softer brake on gravel/water. Default 0.25.":
        "越低 = 碎石/水面刹车越软。默认0.25。",
    "Turbo lag": "涡轮迟滞",
    "Turbo lag vibration": "涡轮迟滞振动",
    "Rumble speed (Hz)": "轰鸣速度 (Hz)",
    "Rumble strength": "轰鸣强度",
    "Boost change sensitivity": "增压变化灵敏度",
    "Brief R2 rumble when boost pressure climbs.":
        "增压压力上升时R2短暂轰鸣。",
    "Deep rumble frequency. Default 8.":
        "低沉轰鸣频率。默认8。",
    "Max vibration amplitude. Default 40.":
        "最大振动幅度。默认40。",
    "Min boost delta per tick to trigger. Default 0.05.":
        "每次触发最小增压变化量。默认0.05。",
    "Cooldown (ms)": "冷却时间 (ms)",
    "Min gap between rumbles. Suppresses steady-state jitter. Default 300.":
        "振动间最短间隔。抑制稳态抖动。默认300。",
}
