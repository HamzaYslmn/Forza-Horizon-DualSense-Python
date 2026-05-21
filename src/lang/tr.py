# -*- coding: utf-8 -*-
"""Türkçe (Turkish) catalog. Keys are the English source strings."""

NAME = "Türkçe"

STRINGS = {
    # --- chrome / tabs ---
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
    "active": "etkin",
    "(none)": "(yok)",
    "Backend failed: {error}": "Backend başlatılamadı: {error}",
    "Profile: {name}": "Profil: {name}",
    "Active: {name}": "Etkin: {name}",

    # --- settings tab sections ---
    "Pedal dead zones": "Pedal ölü bölgeleri",
    "Left trigger - Brake force": "Sol tetik - Fren gücü",
    "Left trigger - Static wall (optional)": "Sol tetik - Statik duvar (opsiyonel)",
    "Right trigger - Gas force": "Sağ tetik - Gaz gücü",
    "ABS (anti-lock brake) rumble": "ABS (kilitlenme önleyici fren) titreşimi",
    "Redline (rev limiter) buzz": "Devir sınırı (redline) titreşimi",
    "Wheelspin buzz": "Patinaj titreşimi",
    "Gear shift thump": "Vites darbesi",

    # --- settings tab fields ---
    "Gas trigger dead zone": "Gaz tetiği ölü bölgesi",
    "Brake trigger dead zone": "Fren tetiği ölü bölgesi",
    "Resting stiffness": "Bekleme sertliği",
    "Hard-press stiffness": "Tam basınç sertliği",
    "Stiffness curve shape": "Sertlik eğrisi şekli",
    "Handbrake extra stiffness": "El freni ek sertliği",
    "Wall position on the trigger": "Tetik üzerindeki duvar konumu",
    "Wall hardness": "Duvar sertliği",
    "Only when braking harder than": "Yalnızca şundan sert frende",
    "Only when faster than (km/h)": "Yalnızca şundan hızlıyken (km/s)",
    "Wheel slip sensitivity": "Tekerlek kayma hassasiyeti",
    "Tire grip sensitivity": "Lastik tutuş hassasiyeti",
    "Rumble speed (Hz)": "Titreşim hızı (Hz)",
    "Rumble strength": "Titreşim gücü",
    "Fire near redline at": "Devir sınırına yakın tetikle",
    "Buzz speed (Hz)": "Vızıltı hızı (Hz)",
    "Buzz strength": "Vızıltı gücü",
    "Buzz hold time (ms)": "Vızıltı tutma süresi (ms)",
    "Thump speed (Hz)": "Darbe hızı (Hz)",
    "Thump strength": "Darbe gücü",
    "Thump length (ms)": "Darbe süresi (ms)",

    # --- settings tab buttons / hints ---
    "Reset to defaults": "Varsayılanlara sıfırla",
    "Click again to confirm reset": "Sıfırlamayı onaylamak için tekrar tıklayın",
    "In Forza HUD: host 127.0.0.1 (try ::1 if it fails).":
        "Forza HUD'da host 127.0.0.1 olmalı (çalışmazsa ::1 deneyin).",
    "UDP port {port} is in use. Close the other listener or change the port in the System tab.":
        "UDP {port} bağlantı noktası kullanımda. Diğer dinleyiciyi kapatın ya da Sistem sekmesinden portu değiştirin.",

    # --- system tab sections / fields ---
    "Telemetry (applies on next launch)": "Telemetri (sonraki açılışta uygulanır)",
    "Startup pulse": "Başlangıç titreşimi",
    "Reconnect": "Yeniden bağlan",
    "Game detection": "Oyun algılama",
    "UDP port": "UDP bağlantı noktası",
    "Startup buzz strength": "Başlangıç vızıltı gücü",
    "Auto-reconnect when controller drops": "Kumanda düşerse otomatik yeniden bağlan",
    "Reconnect check interval (s)": "Yeniden bağlanma kontrol aralığı (s)",
    "Auto-exit when the game closes": "Oyun kapanınca otomatik çık",
    "Game-watch check interval (s)": "Oyun izleme kontrol aralığı (s)",

    # --- system tab controller block ---
    "Controller": "Kumanda",
    "Lock to controller": "Kumandaya kilitle",
    "Rescan": "Yeniden tara",
    "Auto (first found)": "Otomatik (ilk bulunan)",
    "attached now": "şu an bağlı",
    "(no serial - not selectable)": "(seri yok - seçilemez)",

    # --- system tab updates block ---
    "Updates": "Güncellemeler",
    "Check for updates at launch": "Açılışta güncellemeleri denetle",
    "When off, ZUV will not prompt for updates on startup. Toggle on and restart the app to check for a new release.":
        "Kapalıyken ZUV açılışta güncelleme sormaz. Yeni sürümü denetlemek için açın ve uygulamayı yeniden başlatın.",
    "ZUV not found: this build is not running inside a ZUV bundle (ZUV_CACHE_ROOT env var is missing), so the update toggle has nothing to control. Run the bundled .zuv.py to manage updates.":
        "ZUV bulunamadı: bu sürüm bir ZUV paketi içinde çalışmıyor (ZUV_CACHE_ROOT ortam değişkeni eksik), bu yüzden güncelleme anahtarının denetleyeceği bir şey yok. Güncellemeleri yönetmek için paketlenmiş .zuv.py dosyasını çalıştırın.",

    # --- system tab DSX block ---
    "DSX output": "DSX çıkışı",
    "Force DSX output (auto-detected when DSX is running)": "DSX çıkışını zorla (DSX çalışıyorsa otomatik algılanır)",
    "DSX is used automatically when DSX.exe is detected. Enable this to force DSX even when not detected.":
        "DSX.exe algılandığında otomatik kullanılır. Algılanmasa bile zorlamak için etkinleştirin.",
    "Auto-detect DSX port": "DSX portunu otomatik algıla",
    "Reads DSX_UDP_PortNumber.txt from %LOCALAPPDATA%\\DSX.":
        "%LOCALAPPDATA%\\DSX konumundaki DSX_UDP_PortNumber.txt dosyasını okur.",
    "DSX host": "DSX sunucusu",
    "DSX port": "DSX portu",
    "Controller index": "Kumanda indeksi",
    "DSX: checking...": "DSX: kontrol ediliyor...",
    "DSX: running": "DSX: çalışıyor",
    "DSX: not detected": "DSX: algılanamadı",
    "Refresh": "Yenile",
    "[bold red]DSX open failed — HID fallback[/]": "[bold red]DSX başlatılamadı — HID kullanılıyor[/]",

    # --- profiles tab ---
    "Load": "Yükle",
    "Rename": "Yeniden adlandır",
    "Delete": "Sil",
    "Save": "Kaydet",
    "New profile name": "Yeni profil adı",
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
