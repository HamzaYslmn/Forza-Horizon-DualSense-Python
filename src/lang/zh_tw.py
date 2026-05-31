# -*- coding: utf-8 -*-
"""繁體中文 (Traditional Chinese, Taiwan) catalog. Keys are the English source strings."""

NAME = "繁體中文"

STRINGS = {
    # --- chrome / tabs ---
    "Controls": "控制",
    "Profiles": "設定檔",
    "Settings": "設定",
    "System": "系統",
    "Language": "語言",
    "Logs": "日誌",
    "Quit": "離開",
    "♥ Sponsor": "♥ 贊助",
    "Changelog": "更新日誌",
    "connected": "已連線",
    "waiting": "等待中",
    "active": "使用中",
    "(none)": "（無）",
    "Backend failed: {error}": "後端啟動失敗：{error}",
    "Profile: {name}": "設定檔：{name}",
    "Active: {name}": "使用中：{name}",

    # --- controls tab (per-trigger effect switches) ---
    "Shift thump": "換檔衝擊",
    "ABS rumble": "ABS 震動",
    "Static brake wall": "煞車靜態防護牆",
    "Brake stiffness": "煞車阻力",
    "Handbrake stiffness bonus": "手煞車額外阻力",
    "Redline buzz": "紅線震動",
    "Wheelspin buzz": "打滑震動",
    "Idle buzz": "怠速震動",
    "Throttle stiffness": "油門阻力",

    # --- settings tab sections ---
    "Pedal dead zones": "踏板死區",
    "Left trigger - Brake force": "左板機 - 煞車力道",
    "Left trigger - Static wall (optional)": "左板機 - 靜態防護牆（選用）",
    "Right trigger - Gas force": "右板機 - 油門力道",
    "ABS (anti-lock brake) rumble": "ABS（防鎖死煞車）震動",
    "Redline (rev limiter) buzz": "紅線（轉速限制器）震動",
    "Wheelspin buzz": "打滑震動",
    "Idle buzz": "怠速震動",
    "Gear shift thump": "換檔衝擊",

    # --- settings tab fields ---
    "Gas trigger dead zone": "油門板機死區",
    "Brake trigger dead zone": "煞車板機死區",
    "Resting stiffness": "靜止阻力",
    "Hard-press stiffness": "重壓阻力",
    "Stiffness curve shape": "阻力曲線形狀",
    "Handbrake extra stiffness": "手煞車額外阻力",
    "Wall position on the trigger": "板機防護牆位置",
    "Wall hardness": "防護牆硬度",
    "Only when braking harder than": "僅在煞車力道大於：",
    "Only when faster than (km/h)": "僅在車速大於 (km/h)：",
    "Wheel slip sensitivity": "打滑靈敏度",
    "Tire grip sensitivity": "輪胎抓地靈敏度",
    "Rumble speed (Hz)": "震動速度 (Hz)",
    "Rumble strength": "震動強度",
    "Fire near redline at": "接近紅線區時觸發",
    "Buzz speed (Hz)": "嗡鳴速度 (Hz)",
    "Buzz strength": "嗡鳴強度",
    "Buzz hold time (ms)": "嗡鳴持續時間 (ms)",
    "Idle strength": "怠速強度",
    "Thump speed (Hz)": "衝擊速度 (Hz)",
    "Thump strength": "衝擊強度",
    "Thump length (ms)": "衝擊長度 (ms)",

    # --- settings tab buttons / hints ---
    "Reset to defaults": "恢復預設值",
    "Click again to confirm reset": "再點一次以確認重設",
    "In Forza HUD: host 127.0.0.1 (try ::1 if it fails).":
        "在 Forza HUD 中：主機設為 127.0.0.1（若無效，請嘗試 ::1）。",
    "UDP port {port} is in use. Close the other listener or change the port in the System tab.":
        "UDP 連接埠 {port} 已被佔用。請關閉其他監聽程式，或在系統頁籤中更改連接埠。",

    # --- system tab sections / fields ---
    "Telemetry (applies on next launch)": "遙測（下次啟動時生效）",
    "Startup pulse": "啟動震動",
    "Reconnect": "重新連線",
    "Game detection": "遊戲偵測",
    "UDP port": "UDP 連接埠",
    "Startup buzz strength": "啟動嗡鳴強度",
    "Auto-reconnect when controller drops": "控制器斷線時自動重新連線",
    "Reconnect check interval (s)": "重新連線檢查間隔 (秒)",
    "Auto-exit when the game closes": "遊戲關閉時自動離開",
    "Game-watch check interval (s)": "遊戲監控檢查間隔 (秒)",

    # --- system tab controller block ---
    "Controller": "控制器",
    "Lock to controller": "鎖定控制器",
    "Rescan": "重新掃描",
    "Auto (first found)": "自動（優先偵測到的）",
    "attached now": "當前已連線",
    "(no serial - not selectable)": "（無序號 - 無法選取）",

    # --- system tab updates block ---
    "Updates": "更新",
    "Check for updates at launch": "啟動時檢查更新",
    "When off, ZUV will not prompt for updates on startup. Toggle on and restart the app to check for a new release.":
        "關閉時，ZUV 不會在啟動時提示更新。開啟並重新啟動應用程式以檢查新版本。",
    "ZUV not found: this build is not running inside a ZUV bundle (ZUV_CACHE_ROOT env var is missing), so the update toggle has nothing to control. Run the bundled .zuv.py to manage updates.":
        "找不到 ZUV：此版本未在 ZUV 套件中執行（缺少 ZUV_CACHE_ROOT 環境變數），因此更新開關無效。請執行打包的 .zuv.py 來管理更新。",

    # --- profiles tab ---
    "Load": "載入",
    "Rename": "重新命名",
    "Delete": "刪除",
    "Save": "儲存",
    "New profile name": "新設定檔名稱",
    "File: {path}": "檔案：{path}",
    "Note: the [b]Default[/] profile is reset to built-in values every time the app launches so new features and tuning come through. System settings (System tab) are preserved. To keep your own tuning across launches, save it as a named profile here.":
        "注意：[b]Default[/] 設定檔會在每次啟動應用程式時重設為內建值，以確保新功能與調校能順利套用。系統設定（系統頁籤）則會保留。若要保留您自己的調校設定，請另存為新的設定檔。",

    # --- logs tab ---
    "level": "層級",
    "pause": "暫停",
    "resume": "繼續",
    "clear": "清除",

    # --- language tab ---
    "Pick a language, then restart the app to apply it.":
        "選擇語言，然後重新啟動應用程式以套用設定。",
    "Restart the app to apply the new language.":
        "重新啟動應用程式以套用新語言。",
}