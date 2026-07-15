# -*- coding: utf-8 -*-
"""繁體中文（台灣）catalog. Keys are the English source strings."""

NAME = "繁體中文（台灣）"

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
    "Static brake wall": "固定煞車阻力牆",
    "Brake stiffness": "煞車阻力",
    "Handbrake stiffness bonus": "手煞車額外阻力",
    "Redline buzz": "紅線震動",
    "Wheelspin buzz": "輪胎打滑震動",
    "Idle buzz": "怠速震動",
    "Throttle stiffness": "油門阻力",
    "LED Lighting": "LED 燈效",
    "LightBar": "燈條",
    "Player LED": "玩家 LED",
    "ABS Light": "ABS 指示燈",

    # --- settings tab sections ---
    "Pedal dead zones": "踏板死區",
    "Left trigger - Brake force": "左扳機 - 煞車力道",
    "Left trigger - Static wall (optional)": "左扳機 - 固定阻力牆（選用）",
    "Right trigger - Gas force": "右扳機 - 油門力道",
    "ABS (anti-lock brake) rumble": "ABS（防鎖死煞車）震動",
    "Redline (rev limiter) buzz": "紅線（轉速限制）震動",
    "Wheelspin buzz": "輪胎打滑震動",
    "Idle buzz": "怠速震動",
    "Gear shift thump": "換檔衝擊",
    "LED Shift Light": "LED 換檔燈",

    # --- settings tab fields ---
    "Gas trigger dead zone": "油門扳機死區",
    "Brake trigger dead zone": "煞車扳機死區",
    "Resting stiffness": "靜止阻力",
    "Hard-press stiffness": "深踩阻力",
    "Stiffness curve shape": "阻力曲線形狀",
    "Handbrake extra stiffness": "手煞車額外阻力",
    "Wall position on the trigger": "扳機上的阻力牆位置",
    "Wall hardness": "阻力牆硬度",
    "Only when braking harder than": "煞車力道高於此值時",
    "Only when faster than (km/h)": "車速高於此值時 (km/h)",
    "Wheel slip sensitivity": "輪胎滑移靈敏度",
    "Tire grip sensitivity": "輪胎抓地靈敏度",
    "Rumble speed (Hz)": "震動速度 (Hz)",
    "Rumble strength": "震動強度",
    "Fire near redline at": "接近紅線時觸發",
    "Buzz speed (Hz)": "震動速度 (Hz)",
    "Buzz strength": "震動強度",
    "Buzz hold time (ms)": "震動持續時間 (ms)",
    "Idle strength": "怠速強度",
    "Thump speed (Hz)": "衝擊速度 (Hz)",
    "Thump strength": "衝擊強度",
    "Thump length (ms)": "衝擊時間 (ms)",
    # === 新增：動態紅線偵測設定 ===
    "Auto-detect true redline": "自動偵測真實紅線",
    "Print detection debug info": "列印偵測除錯資訊",
    "Samples required to lock": "鎖定所需樣本數",
    "RPM clustering tolerance": "RPM 聚類容差",
    # === 新增：LED 換檔燈設定 ===
    "Green zone threshold": "綠區閾值",
    "Orange zone threshold": "橙區閾值",
    "Red zone threshold": "紅區閾值",
    "Flash threshold": "閃爍閾值",

    # --- settings tab buttons / hints ---
    "Reset to defaults": "重設為預設值",
    "Click again to confirm reset": "再按一次確認重設",
    "In Forza HUD: host 127.0.0.1 (try ::1 if it fails).":
        "在 Forza HUD 中: host 設為 127.0.0.1（不行的話試試 ::1）。",
    "Forward telemetry": "轉發遙測資料",
    "Mirror every received packet to another app (e.g. SimHub) without taking the port from it.":
        "將收到的每個封包鏡像到另一個應用程式（如 SimHub），且不佔用連接埠。",
    "Forward to": "轉發到",
    "host:port targets, comma-separated. Default 127.0.0.1:5301.":
        "host:port 目標，以逗號分隔。預設 127.0.0.1:5301。",
    "UDP port {port} is in use. Close the other listener or change the port in the System tab.":
        "UDP 連接埠 {port} 已被使用。請關閉其他監聽程式，或到系統分頁更改連接埠。",
    # === 新增：設定項的提示文本 (Tooltips) ===
    "Dynamically detects rev limiter instead of using dashboard max RPM.": 
        "動態偵測斷油轉速，而不是使用儀表板上的最大轉速。",
    "Outputs redline detection state changes to the console.": 
        "在主控台輸出紅線偵測的狀態變化資訊。",
    "Number of valid peaks needed to lock the true redline.": 
        "鎖定真實紅線所需的有效峰值樣本數量。",
    "Max RPM difference to consider peaks as the same redline.": 
        "被視為同一紅線的最大 RPM 差值（聚類容差）。",

    # --- system tab sections / fields ---
    "Forza telemetry (applies on next launch)": "Forza 遙測（下次啟動生效）",
    "Startup pulse": "啟動震動",
    "Reconnect": "重新連線",
    "Game detection": "遊戲偵測",
    "UDP port": "UDP 連接埠",
    "Startup buzz strength": "啟動震動強度",
    "Auto-reconnect when controller drops": "手把斷線時自動重新連線",
    "Reconnect check interval (s)": "重新連線檢查間隔（秒）",
    "Auto-exit when the game closes": "遊戲關閉時自動離開",
    "Game-watch check interval (s)": "遊戲監看檢查間隔（秒）",

    # --- DSX ---
    "DSX": "DSX",
    "DSX integration": "DSX 整合",
    "Send triggers to DualSenseX over UDP. Takes effect immediately.":
        "透過 UDP 將扳機效果送到 DualSenseX。會立即生效。",
    "DSX connection": "DSX 連線",
    "Host": "主機",
    "Port": "連接埠",
    "Default 127.0.0.1. Match the host in DSX settings.":
        "預設為 127.0.0.1。需與 DSX 設定中的主機一致。",
    "Default 6969. Match the port in DSX settings.":
        "預設為 6969。需與 DSX 設定中的連接埠一致。",
    "DSX is active - controller managed by DSX. Disable DSX to select a controller here.":
        "DSX 已啟用 - 手把由 DSX 管理。停用 DSX 後才能在這裡選擇手把。",
    "DSX: active": "DSX：已啟用",
    "DSX: off": "DSX：已關閉",

    # --- system tab controller block ---
    "Controller": "手把",
    "Lock to controller": "鎖定手把",
    "Rescan": "重新掃描",
    "Auto (first found)": "自動（第一個找到的）",
    "attached now": "目前已連接",
    "(no serial - not selectable)": "（無序號 - 無法選擇）",

    # --- system tab updates block ---
    "Updates": "更新",
    "Check for updates at launch": "啟動時檢查更新",
    "When off, ZUV will not prompt for updates on startup. Toggle on and restart the app to check for a new release.":
        "關閉時，ZUV 不會在啟動時提示更新。開啟後重新啟動應用程式，即可檢查新版本。",
    "ZUV not found: this build is not running inside a ZUV bundle (ZUV_CACHE_ROOT env var is missing), so the update toggle has nothing to control. Run the bundled .zuv.py to manage updates.":
        "找不到 ZUV：這個版本不是在 ZUV bundle 內執行（缺少 ZUV_CACHE_ROOT 環境變數），所以更新開關沒有可控制的項目。請執行打包的 .zuv.py 來管理更新。",

    # --- profiles tab ---
    "Load": "載入",
    "Rename": "重新命名",
    "Delete": "刪除",
    "Save": "儲存",
    "New profile name": "新設定檔名稱",
    "File: {path}": "檔案：{path}",
    "Note: the [b]Default[/] profile is reset to built-in values every time the app launches so new features and tuning come through. System settings (System tab) are preserved. To keep your own tuning across launches, save it as a named profile here.":
        "注意：[b]Default[/] 設定檔會在每次啟動時重設為內建值，讓新功能與調校能套用進來。系統設定（系統分頁）會保留。若要在每次啟動後保留自己的調校，請在這裡另存成具名設定檔。",
    "Profile": "設定檔",
    "Saved profiles": "已儲存的設定檔",
    "Save current settings": "儲存目前設定",
    "Save profile": "儲存設定檔",
    "Share profile": "分享設定檔",
    "Export & Copy": "匯出並複製",
    "Import": "匯入",
    "Export the selected profile as a short code (copied to your clipboard), or paste a code below and import it.":
        "將選取的設定檔匯出成短代碼（並複製到剪貼簿），或在下方貼上代碼後匯入。",
    "Save and switch named snapshots of your settings.":
        "儲存並切換具名的設定快照。",
    "The Default profile resets on every launch to pick up new features and tuning. System tab settings are preserved. Save a named profile to keep your own tuning.":
        "Default 設定檔會在每次啟動時重設，以套用新功能與調校。系統分頁設定會保留。請儲存具名設定檔來保留自己的調校。",
    "No profile selected.": "尚未選擇設定檔。",
    "Copied {name} to clipboard.": "已將 {name} 複製到剪貼簿。",
    "Copy failed. Select the code and copy manually.": "複製失敗。請選取代碼後手動複製。",
    "Export failed.": "匯出失敗。",
    "Paste a code first.": "請先貼上代碼。",
    "Invalid share code.": "分享代碼無效。",
    "Imported as {name}.": "已匯入為 {name}。",

    # --- controls / system descriptions ---
    "Toggle individual trigger effects. Changes save instantly.":
        "個別開關扳機效果。變更會立即儲存。",
    "Lock the app to a specific DualSense, or let it pick the first one.":
        "將應用程式鎖定到特定 DualSense，或讓它自動選擇第一個找到的手把。",
    "UDP port {port} in use": "UDP 連接埠 {port} 使用中",

    # --- logs tab ---
    "Level": "等級",
    "level": "等級",
    "pause": "暫停",
    "resume": "繼續",
    "clear": "清除",
    "latched": "已鎖定",
    "Live application output. Increase verbosity for debugging.":
        "即時應用程式輸出。除錯時可提高詳細程度。",

    # --- language tab ---
    "Available languages": "可用語言",
    "Pick a language, then restart the app to apply it.":
        "選擇語言後，重新啟動應用程式即可套用。",
    "Restart the app to apply your choice.":
        "重新啟動應用程式以套用你的選擇。",
    "Restart the app to apply the new language.":
        "重新啟動應用程式以套用新語言。",

    # --- external links ---
    "Sponsor": "贊助",
}
