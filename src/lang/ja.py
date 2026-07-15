# -*- coding: utf-8 -*-
"""日本語 (Japanese) catalog. Keys are the English source strings."""

NAME = "日本語"

STRINGS = {
    # --- chrome / tabs ---
    "Controls": "操作",
    "Profiles": "プロファイル",
    "Settings": "設定",
    "System": "システム",
    "Language": "言語",
    "Logs": "ログ",
    "Quit": "終了",
    "♥ Sponsor": "♥ 支援",
    "Changelog": "変更履歴",
    "connected": "接続済み",
    "waiting": "待機中",
    "active": "使用中",
    "(none)": "（なし）",
    "Backend failed: {error}": "バックエンドの起動に失敗しました: {error}",
    "Profile: {name}": "プロファイル: {name}",
    "Active: {name}": "使用中: {name}",

    # --- controls tab (per-trigger effect switches) ---
    "Shift thump": "シフトショック",
    "ABS rumble": "ABS 振動",
    "Static brake wall": "ブレーキの固定ウォール",
    "Brake stiffness": "ブレーキの硬さ",
    "Handbrake stiffness bonus": "ハンドブレーキの追加の硬さ",
    "Redline buzz": "レッドライン振動",
    "Wheelspin buzz": "ホイールスピン振動",
    "Idle buzz": "アイドリング振動",
    "Throttle stiffness": "アクセルの硬さ",
    "LED Lighting": "LED照明",
    "LightBar": "RGBライトバー",
    "Player LED": "プレイヤーLED",
    "ABS Light": "ABSインジケーター",

    # --- settings tab sections ---
    "Pedal dead zones": "ペダルのデッドゾーン",
    "Left trigger - Brake force": "左トリガー - ブレーキの強さ",
    "Left trigger - Static wall (optional)": "左トリガー - 固定ウォール（任意）",
    "Right trigger - Gas force": "右トリガー - アクセルの強さ",
    "ABS (anti-lock brake) rumble": "ABS（アンチロックブレーキ）振動",
    "Redline (rev limiter) buzz": "レッドライン（レブリミッター）振動",
    "Wheelspin buzz": "ホイールスピン振動",
    "Idle buzz": "アイドリング振動",
    "Gear shift thump": "シフトショック",
    "LED Shift Light": "LEDシフトライト",

    # --- settings tab fields ---
    "Gas trigger dead zone": "アクセルトリガーのデッドゾーン",
    "Brake trigger dead zone": "ブレーキトリガーのデッドゾーン",
    "Resting stiffness": "待機時の硬さ",
    "Hard-press stiffness": "深押し時の硬さ",
    "Stiffness curve shape": "硬さカーブの形状",
    "Handbrake extra stiffness": "ハンドブレーキの追加の硬さ",
    "Wall position on the trigger": "トリガー上のウォール位置",
    "Wall hardness": "ウォールの硬さ",
    "Only when braking harder than": "ブレーキ強度が次を超えるときのみ",
    "Only when faster than (km/h)": "速度が次を超えるときのみ (km/h)",
    "Wheel slip sensitivity": "ホイールスリップ感度",
    "Tire grip sensitivity": "タイヤグリップ感度",
    "Rumble speed (Hz)": "振動の速さ (Hz)",
    "Rumble strength": "振動の強さ",
    "Fire near redline at": "レッドライン付近で発動",
    "Buzz speed (Hz)": "振動の速さ (Hz)",
    "Buzz strength": "振動の強さ",
    "Buzz hold time (ms)": "振動の保持時間 (ms)",
    "Idle strength": "アイドリングの強さ",
    "Thump speed (Hz)": "ショックの速さ (Hz)",
    "Thump strength": "ショックの強さ",
    "Thump length (ms)": "ショックの長さ (ms)",
    "Auto-detect true redline": "本当のレッドラインを自動検出",
    "Print detection debug info": "検出デバッグ情報を出力",
    "Samples required to lock": "ロックに必要なサンプル数",
    "RPM clustering tolerance": "RPMクラスタリング許容差",
    "Green zone threshold": "グリーンゾーン閾値",
    "Orange zone threshold": "オレンジゾーン閾値",
    "Red zone threshold": "レッドゾーン閾値",
    "Flash threshold": "フラッシュ閾値",

    # --- settings tab buttons / hints ---
    "Reset to defaults": "デフォルトに戻す",
    "Click again to confirm reset": "もう一度クリックしてリセットを確定",
    "In Forza HUD: host 127.0.0.1 (try ::1 if it fails).":
        "Forza HUD で host を 127.0.0.1 に設定（うまくいかなければ ::1 を試す）。",
    "Forward telemetry": "テレメトリを転送",
    "Mirror every received packet to another app (e.g. SimHub) without taking the port from it.":
        "受信した各パケットを別のアプリ（例: SimHub）にミラーします。ポートを奪いません。",
    "Forward to": "転送先",
    "host:port targets, comma-separated. Default 127.0.0.1:5301.":
        "host:port 形式の宛先（カンマ区切り）。既定値 127.0.0.1:5301。",
    "UDP port {port} is in use. Close the other listener or change the port in the System tab.":
        "UDP ポート {port} は使用中です。他のリスナーを閉じるか、システムタブでポートを変更してください。",

    # --- system tab sections / fields ---
    "Forza telemetry (applies on next launch)": "Forza テレメトリ（次回起動時に適用）",
    "Startup pulse": "起動時の振動",
    "Reconnect": "再接続",
    "Game detection": "ゲーム検出",
    "UDP port": "UDP ポート",
    "Startup buzz strength": "起動時の振動の強さ",
    "Auto-reconnect when controller drops": "コントローラー切断時に自動再接続",
    "Reconnect check interval (s)": "再接続の確認間隔 (秒)",
    "Auto-exit when the game closes": "ゲーム終了時に自動終了",
    "Game-watch check interval (s)": "ゲーム監視の確認間隔 (秒)",

    # --- DSX ---
    "DSX": "DSX",
    "DSX integration": "DSX 連携",
    "Send triggers to DualSenseX over UDP. Takes effect immediately.":
        "UDP 経由でトリガーを DualSenseX に送信。即座に反映されます。",
    "DSX connection": "DSX 接続",
    "Host": "ホスト",
    "Port": "ポート",
    "Default 127.0.0.1. Match the host in DSX settings.":
        "デフォルト 127.0.0.1。DSX 設定のホストと一致させる必要があります。",
    "Default 6969. Match the port in DSX settings.":
        "デフォルト 6969。DSX 設定のポートと一致させる必要があります。",
    "DSX is active - controller managed by DSX. Disable DSX to select a controller here.":
        "DSX が有効 - コントローラーは DSX が管理中。コントローラーを選択するには DSX を無効にしてください。",
    "DSX: active": "DSX: 有効",
    "DSX: off": "DSX: オフ",

    # --- system tab controller block ---
    "Controller": "コントローラー",
    "Lock to controller": "コントローラーに固定",
    "Rescan": "再スキャン",
    "Auto (first found)": "自動（最初に見つかったもの）",
    "attached now": "現在接続中",
    "(no serial - not selectable)": "（シリアルなし - 選択不可）",

    # --- system tab updates block ---
    "Updates": "アップデート",
    "Check for updates at launch": "起動時に更新を確認",
    "When off, ZUV will not prompt for updates on startup. Toggle on and restart the app to check for a new release.":
        "オフの場合、ZUV は起動時に更新を確認しません。新しいリリースを確認するにはオンにしてアプリを再起動してください。",
    "ZUV not found: this build is not running inside a ZUV bundle (ZUV_CACHE_ROOT env var is missing), so the update toggle has nothing to control. Run the bundled .zuv.py to manage updates.":
        "ZUV が見つかりません: このビルドは ZUV バンドル内で実行されていません（ZUV_CACHE_ROOT 環境変数がありません）。更新トグルが制御する対象がないため、更新を管理するにはバンドルされた .zuv.py を実行してください。",

    # --- profiles tab ---
    "Load": "読み込み",
    "Rename": "名前変更",
    "Delete": "削除",
    "Save": "保存",
    "New profile name": "新しいプロファイル名",
    "File: {path}": "ファイル: {path}",
    "Note: the [b]Default[/] profile is reset to built-in values every time the app launches so new features and tuning come through. System settings (System tab) are preserved. To keep your own tuning across launches, save it as a named profile here.":
        "注意: [b]Default[/] プロファイルは、新機能や調整を反映するためアプリ起動のたびに組み込み値へリセットされます。システム設定（システムタブ）は保持されます。独自の調整を起動間で保持するには、ここで名前付きプロファイルとして保存してください。",
    "Dynamically detects rev limiter instead of using dashboard max RPM.":
        "ダッシュボードの最大RPMを使用する代わりに、アルゴリズムでレブリミッターを識別します。",
    "Outputs redline detection state changes to the console.":
        "レッドライン検出の状態変化をコンソールに出力します。",
    "Number of valid peaks needed to lock the true redline.":
        "真のレッドラインをロックするために必要な有効なピークサンプル数。",
    "Max RPM difference to consider peaks as the same redline.":
        "ピークを同一のレッドラインとみなすための最大RPM差（クラスタリング許容差）。",

    # --- logs tab ---
    "level": "レベル",
    "pause": "一時停止",
    "resume": "再開",
    "clear": "クリア",

    # --- language tab ---
    "Pick a language, then restart the app to apply it.":
        "言語を選択し、アプリを再起動して適用してください。",
    "Restart the app to apply the new language.":
        "新しい言語を適用するにはアプリを再起動してください。",
}
