# -*- coding: utf-8 -*-
"""日本語 (Japanese) catalog. Keys are the English source strings."""

NAME = "日本語"

STRINGS = {
    # --- tabs / chrome ---
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
    "Backend failed: {error}": "バックエンド起動失敗: {error}",
    "Profile: {name}": "プロファイル: {name}",
    "(none)": "（なし）",
    "active": "使用中",

    # --- controls tab ---
    "Brake stiffness": "ブレーキ剛性",
    "Static brake wall": "静的ブレーキウォール",
    "Handbrake stiffness bonus": "ハンドブレーキ剛性ボーナス",
    "ABS rumble": "ABS 振動",
    "Shift thump": "シフトショック",
    "Throttle stiffness": "スロットル剛性",
    "Redline buzz": "レッドライン振動",
    "Wheelspin pulse": "ホイールスピンパルス",

    # --- settings sections ---
    "Pedals / deadzones": "ペダル / デッドゾーン",
    "Brake (left trigger)": "ブレーキ（左トリガー）",
    "Throttle (right trigger)": "スロットル（右トリガー）",
    "Rev limiter": "レブリミッター",
    "Gear shift thump": "シフトショック",

    # --- settings fields ---
    "Accel deadzone": "アクセルデッドゾーン",
    "Brake deadzone": "ブレーキデッドゾーン",
    "Baseline force": "基準フォース",
    "Max force": "最大フォース",
    "Curve": "カーブ",
    "Static wall at": "静的ウォール位置",
    "Static wall force": "静的ウォール強度",
    "Handbrake bonus": "ハンドブレーキボーナス",
    "Brake threshold": "ブレーキしきい値",
    "Min speed (km/h)": "最低速度 (km/h)",
    "Slip ratio threshold": "スリップ率しきい値",
    "Combined slip threshold": "複合スリップしきい値",
    "Frequency (Hz)": "周波数 (Hz)",
    "Amplitude": "振幅",
    "Trigger at RPM ratio": "RPM 比で作動",
    "Hold (ms)": "保持 (ms)",
    "Duration (ms)": "継続 (ms)",
    "Min throttle": "最小スロットル",
    "Slip threshold": "スリップしきい値",
    "Slip full-scale range": "スリップフルスケール範囲",

    # --- system sections / fields ---
    "Telemetry (applies on next launch)": "テレメトリ（次回起動時に適用）",
    "Startup pulse": "起動パルス",
    "Reconnect": "再接続",
    "Game detection": "ゲーム検出",
    "UDP port": "UDP ポート",
    "Startup pulse force": "起動パルス強度",
    "Auto-reconnect controller (disable for HidHide)": "コントローラー自動再接続（HidHide 時は無効化）",
    "Reconnect interval (s)": "再接続間隔 (秒)",
    "Detect game (auto-exit when it closes)": "ゲームを検出（終了時に自動終了）",
    "Poll interval (s)": "ポーリング間隔 (秒)",
    "Reset to defaults": "デフォルトに戻す",

    # --- updates (top of System tab) ---
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
    "Active: {name}": "使用中: {name}",
    "File: {path}": "ファイル: {path}",
    "Note: the [b]Default[/] profile is reset to built-in values every time the app launches so new features and tuning come through. System settings (System tab) are preserved. To keep your own tuning across launches, save it as a named profile here.":
        "注意: [b]Default[/] プロファイルは、新機能や調整を反映するためアプリ起動のたびに組み込み値へリセットされます。システム設定（システムタブ）は保持されます。独自の調整を起動間で保持するには、ここで名前付きプロファイルとして保存してください。",

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
