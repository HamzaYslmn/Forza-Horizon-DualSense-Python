# -*- coding: utf-8 -*-
"""中文 (Chinese, Simplified) catalog. Keys are the English source strings."""

NAME = "中文"

STRINGS = {
    # --- tabs / chrome ---
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
    "Backend failed: {error}": "后端启动失败：{error}",
    "Profile: {name}": "配置文件：{name}",
    "(none)": "（无）",
    "active": "当前",

    # --- controls tab ---
    "Brake stiffness": "刹车阻力",
    "Static brake wall": "静态刹车墙",
    "Handbrake stiffness bonus": "手刹阻力加成",
    "ABS rumble": "ABS 振动",
    "Shift thump": "换挡冲击",
    "Throttle stiffness": "油门阻力",
    "Redline buzz": "红线区震动",
    "Wheelspin pulse": "打滑脉冲",

    # --- settings sections ---
    "Pedals / deadzones": "踏板 / 死区",
    "Brake (left trigger)": "刹车（左扳机）",
    "Throttle (right trigger)": "油门（右扳机）",
    "Rev limiter": "转速限制器",
    "Gear shift thump": "换挡冲击",

    # --- settings fields ---
    "Accel deadzone": "油门死区",
    "Brake deadzone": "刹车死区",
    "Baseline force": "基础力度",
    "Max force": "最大力度",
    "Curve": "曲线",
    "Static wall at": "静态墙位置",
    "Static wall force": "静态墙力度",
    "Handbrake bonus": "手刹加成",
    "Brake threshold": "刹车阈值",
    "Min speed (km/h)": "最低速度 (km/h)",
    "Slip ratio threshold": "滑移率阈值",
    "Combined slip threshold": "综合滑移阈值",
    "Frequency (Hz)": "频率 (Hz)",
    "Amplitude": "振幅",
    "Trigger at RPM ratio": "在转速比触发",
    "Hold (ms)": "保持 (ms)",
    "Duration (ms)": "持续 (ms)",
    "Min throttle": "最低油门",
    "Slip threshold": "打滑阈值",
    "Slip full-scale range": "打滑满量程范围",

    # --- system sections / fields ---
    "Telemetry (applies on next launch)": "遥测（下次启动生效）",
    "Startup pulse": "启动脉冲",
    "Reconnect": "重新连接",
    "Game detection": "游戏检测",
    "UDP port": "UDP 端口",
    "Startup pulse force": "启动脉冲力度",
    "Auto-reconnect controller (disable for HidHide)": "自动重连手柄（HidHide 时关闭）",
    "Reconnect interval (s)": "重连间隔 (秒)",
    "Detect game (auto-exit when it closes)": "检测游戏（关闭时自动退出）",
    "Poll interval (s)": "轮询间隔 (秒)",
    "Reset to defaults": "恢复默认",

    # --- updates (top of System tab) ---
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
    "Active: {name}": "当前：{name}",
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
}
