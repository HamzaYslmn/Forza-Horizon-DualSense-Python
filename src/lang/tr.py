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

    # --- controls tab (per-trigger effect switches) ---
    "Shift thump": "Vites darbesi",
    "ABS rumble": "ABS titreşimi",
    "Static brake wall": "Sabit fren duvarı",
    "Brake stiffness": "Fren sertliği",
    "Handbrake stiffness bonus": "El freni ek sertliği",
    "Redline buzz": "Devir sınırı titreşimi",
    "Wheelspin buzz": "Patinaj titreşimi",
    "Idle buzz": "Rölanti titreşimi",
    "Throttle stiffness": "Gaz sertliği",
    "LED Lighting": "LED Aydınlatma",
    "LightBar": "RGB Işık Çubuğu",
    "Player LED": "Oyuncu LED'i",
    "ABS Light": "ABS Işığı",

    # --- settings tab sections ---
    "Pedal dead zones": "Pedal ölü bölgeleri",
    "Left trigger - Brake force": "Sol tetik - Fren gücü",
    "Left trigger - Static wall (optional)": "Sol tetik - Sabit duvar (isteğe bağlı)",
    "Right trigger - Gas force": "Sağ tetik - Gaz gücü",
    "ABS (anti-lock brake) rumble": "ABS (kilitlenme önleyici fren) titreşimi",
    "Redline (rev limiter) buzz": "Devir sınırı (redline) titreşimi",
    "Wheelspin buzz": "Patinaj titreşimi",
    "Idle buzz": "Rölanti titreşimi",
    "Gear shift thump": "Vites darbesi",
    "LED Shift Light": "LED Vites Işığı",

    # --- settings tab fields ---
    "Gas trigger dead zone": "Gaz tetiği ölü bölgesi",
    "Brake trigger dead zone": "Fren tetiği ölü bölgesi",
    "Resting stiffness": "Bekleme sertliği",
    "Hard-press stiffness": "Tam basış sertliği",
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
    "Fire near redline at": "Devir sınırına yakın tetikleme",
    "Buzz speed (Hz)": "Titreşim hızı (Hz)",
    "Buzz strength": "Titreşim gücü",
    "Buzz hold time (ms)": "Titreşim tutma süresi (ms)",
    "Idle strength": "Rölanti gücü",
    "Thump speed (Hz)": "Darbe hızı (Hz)",
    "Thump strength": "Darbe gücü",
    "Thump length (ms)": "Darbe süresi (ms)",
    "Auto-detect true redline": "Gerçek devir sınırını otomatik algıla",
    "Print detection debug info": "Algılama hata ayıklama bilgisini yazdır",
    "Samples required to lock": "Kilitleme için gereken örnek sayısı",
    "RPM clustering tolerance": "RPM kümeleme toleransı",
    "Green zone threshold": "Yeşil bölge eşiği",
    "Orange zone threshold": "Turuncu bölge eşiği",
    "Red zone threshold": "Kırmızı bölge eşiği",
    "Flash threshold": "Flaş eşiği",

    # --- settings tab buttons / hints ---
    "Reset to defaults": "Varsayılanlara sıfırla",
    "Click again to confirm reset": "Sıfırlamayı onaylamak için tekrar tıklayın",
    "In Forza HUD: host 127.0.0.1 (try ::1 if it fails).":
        "Forza HUD'da host 127.0.0.1 olmalı (çalışmazsa ::1 deneyin).",
    "Forward telemetry": "Telemetriyi ilet",
    "Mirror every received packet to another app (e.g. SimHub) without taking the port from it.":
        "Alınan her paketi, bağlantı noktasını almadan başka bir uygulamaya (ör. SimHub) yansıtır.",
    "Forward to": "Şuraya ilet",
    "host:port targets, comma-separated. Default 127.0.0.1:5301.":
        "host:port hedefleri, virgülle ayrılır. Varsayılan 127.0.0.1:5301.",
    "UDP port {port} is in use. Close the other listener or change the port in the System tab.":
        "UDP portu {port} kullanımda. Diğer dinleyiciyi kapatın ya da Sistem sekmesinden portu değiştirin.",
    "Dynamically detects rev limiter instead of using dashboard max RPM.":
        "Gösterge panelindeki maksimum RPM yerine algoritma ile devir sınırlayıcıyı algılar.",
    "Outputs redline detection state changes to the console.":
        "Kırmızı çizgi algılama durum değişikliklerini konsola yazdırır.",
    "Number of valid peaks needed to lock the true redline.":
        "Gerçek kırmızı çizgiyi kilitlemek için gereken geçerli tepe noktası sayısı.",
    "Max RPM difference to consider peaks as the same redline.":
        "Tepe noktalarını aynı kırmızı çizgi olarak kabul etmek için maksimum RPM farkı (kümeleme toleransı).",

    # --- system tab sections / fields ---
    "Forza telemetry (applies on next launch)": "Forza telemetri (sonraki açılışta uygulanır)",
    "Startup pulse": "Başlangıç titreşimi",
    "Reconnect": "Yeniden bağlanma",
    "Game detection": "Oyun algılama",
    "UDP port": "UDP portu",
    "Startup buzz strength": "Başlangıç titreşim gücü",
    "Auto-reconnect when controller drops": "Kumanda kopunca otomatik yeniden bağlan",
    "Reconnect check interval (s)": "Yeniden bağlanma kontrol aralığı (s)",
    "Auto-exit when the game closes": "Oyun kapanınca otomatik çık",
    "Game-watch check interval (s)": "Oyun izleme kontrol aralığı (s)",

    # --- DSX ---
    "DSX": "DSX",
    "DSX integration": "DSX entegrasyonu",
    "Send triggers to DualSenseX over UDP. Takes effect immediately.":
        "Tetikleri UDP üzerinden DualSenseX'e gönder. Hemen etkinleşir.",
    "DSX connection": "DSX bağlantısı",
    "Host": "Host",
    "Port": "Port",
    "Default 127.0.0.1. Match the host in DSX settings.":
        "Varsayılan 127.0.0.1. DSX ayarlarındaki host ile eşleşmeli.",
    "Default 6969. Match the port in DSX settings.":
        "Varsayılan 6969. DSX ayarlarındaki port ile eşleşmeli.",
    "DSX is active - controller managed by DSX. Disable DSX to select a controller here.":
        "DSX etkin - kumanda DSX tarafından yönetiliyor. Kumanda seçmek için DSX'i devre dışı bırakın.",
    "DSX: active": "DSX: etkin",
    "DSX: off": "DSX: kapalı",

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
