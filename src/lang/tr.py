# -*- coding: utf-8 -*-
"""Türkçe (Turkish) catalog. Keys are the English source strings."""

NAME = "Türkçe"

STRINGS = {
    # --- tabs / chrome ---
    "Controls": "Kontroller",
    "Profiles": "Profiller",
    "Settings": "Ayarlar",
    "System": "Sistem",
    "Language": "Dil",
    "Logs": "Loglar",
    "Quit": "Çıkış",
    "♥ Sponsor": "♥ Destekle",
    "Changelog": "Sürüm Notları",
    "connected": "bağlı",
    "waiting": "bekleniyor",
    "Backend failed: {error}": "Backend başlatılamadı: {error}",
    "Profile: {name}": "Profil: {name}",
    "(none)": "(yok)",
    "active": "etkin",

    # --- controls tab ---
    "Brake stiffness": "Fren sertliği",
    "Static brake wall": "Statik fren duvarı",
    "Handbrake stiffness bonus": "El freni sertlik bonusu",
    "ABS rumble": "ABS titreşimi",
    "Shift thump": "Vites darbesi",
    "Throttle stiffness": "Gaz sertliği",
    "Redline buzz": "Devir sınırı titreşimi",
    "Wheelspin pulse": "Patinaj titreşimi",

    # --- settings sections ---
    "Pedals / deadzones": "Pedallar / ölü bölgeler",
    "Brake (left trigger)": "Fren (sol tetik)",
    "Throttle (right trigger)": "Gaz (sağ tetik)",
    "Rev limiter": "Devir sınırlayıcı",
    "Gear shift thump": "Vites darbesi",

    # --- settings fields ---
    "Accel deadzone": "Gaz ölü bölgesi",
    "Brake deadzone": "Fren ölü bölgesi",
    "Baseline force": "Taban kuvvet",
    "Max force": "Maks kuvvet",
    "Curve": "Eğri",
    "Static wall at": "Statik duvar konumu",
    "Static wall force": "Statik duvar gücü",
    "Handbrake bonus": "El freni bonusu",
    "Brake threshold": "Fren eşiği",
    "Min speed (km/h)": "Min hız (km/s)",
    "Slip ratio threshold": "Kayma oranı eşiği",
    "Combined slip threshold": "Birleşik kayma eşiği",
    "Frequency (Hz)": "Frekans (Hz)",
    "Amplitude": "Genlik",
    "Trigger at RPM ratio": "RPM oranında tetikle",
    "Hold (ms)": "Tutma (ms)",
    "Duration (ms)": "Süre (ms)",
    "Min throttle": "Minimum gaz",
    "Slip threshold": "Kayma eşiği",
    "Slip full-scale range": "Kayma tam ölçek aralığı",

    # --- system sections / fields ---
    "Telemetry (applies on next launch)": "Telemetri (sonraki açılışta uygulanır)",
    "Startup pulse": "Başlangıç titreşimi",
    "Reconnect": "Yeniden bağlan",
    "Game detection": "Oyun algılama",
    "UDP port": "UDP bağlantı noktası",
    "Startup pulse force": "Başlangıç titreşim gücü",
    "Auto-reconnect controller (disable for HidHide)": "Kumandayı otomatik bağla (HidHide için kapatın)",
    "Reconnect interval (s)": "Yeniden bağlanma aralığı (s)",
    "Detect game (auto-exit when it closes)": "Oyunu algıla (kapanınca otomatik çık)",
    "Poll interval (s)": "Yoklama aralığı (s)",
    "Reset to defaults": "Varsayılanlara sıfırla",

    # --- updates (top of System tab) ---
    "Updates": "Güncellemeler",
    "Check for updates at launch": "Açılışta güncellemeleri denetle",
    "When off, ZUV will not prompt for updates on startup. Toggle on and restart the app to check for a new release.":
        "Kapalıyken ZUV açılışta güncelleme sormaz. Yeni sürümü denetlemek için açın ve uygulamayı yeniden başlatın.",
    "ZUV not found: this build is not running inside a ZUV bundle (ZUV_CACHE_ROOT env var is missing), so the update toggle has nothing to control. Run the bundled .zuv.py to manage updates.":
        "ZUV bulunamadı: bu sürüm bir ZUV paketi içinde çalışmıyor (ZUV_CACHE_ROOT ortam değişkeni eksik), bu yüzden güncelleme anahtarının denetleyeceği bir şey yok. Güncellemeleri yönetmek için paketlenmiş .zuv.py dosyasını çalıştırın.",

    # --- profiles tab ---
    "Load": "Yükle",
    "Rename": "Yeniden adlandır",
    "Delete": "Sil",
    "Save": "Kaydet",
    "New profile name": "Yeni profil adı",
    "Active: {name}": "Etkin: {name}",
    "File: {path}": "Dosya: {path}",
    "Note: the [b]Default[/] profile is reset to built-in values every time the app launches so new features and tuning come through. System settings (System tab) are preserved. To keep your own tuning across launches, save it as a named profile here.":
        "Not: [b]Default[/] profili, yeni özellikler ve ayarlar gelsin diye uygulama her açıldığında yerleşik değerlere sıfırlanır. Sistem ayarları (Sistem sekmesi) korunur. Kendi ayarlarınızı açılışlar arasında saklamak için burada adlandırılmış bir profil olarak kaydedin.",

    # --- logs tab ---
    "level": "seviye",
    "pause": "duraklat",
    "resume": "sürdür",
    "clear": "temizle",

    # --- language tab ---
    "Pick a language, then restart the app to apply it.":
        "Bir dil seçin, ardından uygulamak için uygulamayı yeniden başlatın.",
    "Restart the app to apply the new language.":
        "Yeni dili uygulamak için uygulamayı yeniden başlatın.",
}
