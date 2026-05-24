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

    # --- settings tab buttons / hints ---
    "Reset to defaults": "Varsayılanlara sıfırla",
    "Click again to confirm reset": "Sıfırlamayı onaylamak için tekrar tıklayın",
    "In Forza HUD: host 127.0.0.1 (try ::1 if it fails).":
        "Forza HUD'da host 127.0.0.1 olmalı (çalışmazsa ::1 deneyin).",
    "UDP port {port} is in use. Close the other listener or change the port in the System tab.":
        "UDP portu {port} kullanımda. Diğer dinleyiciyi kapatın ya da Sistem sekmesinden portu değiştirin.",

    # --- system tab sections / fields ---
    "Telemetry (applies on next launch)": "Telemetri (sonraki açılışta uygulanır)",
    "Startup pulse": "Başlangıç titreşimi",
    "Reconnect": "Yeniden bağlanma",
    "Game detection": "Oyun algılama",
    "UDP port": "UDP portu",
    "Startup buzz strength": "Başlangıç titreşim gücü",
    "Auto-reconnect when controller drops": "Kumanda kopunca otomatik yeniden bağlan",
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
    "Speed-based throttle": "Hıza dayalı gaz",
    "Extra force at standstill": "Dururken ekstra kuvvet",
    "Fade-out speed (km/h)": "Sönme hızı (km/s)",
    "Extra resistance at low speed for precise control, lighter at high speed.":
        "Düşük hızda hassas kontrol için ekstra direnç, yüksek hızda daha hafif.",
    "0 = off. Flat resistance added at 0 km/h, fading to normal.":
        "0 = kapalı. 0 km/s'de düz direnç eklenir, normale kadar sönür.",
    "Speed where boost fully fades. Default 80.":
        "Takviyenin tamamen söndüğü hız. Varsayılan 80.",
    "Surface brake resistance": "Yüzey freni direnci",
    "Tarmac multiplier": "Asfalt çarpanı",
    "Dirt multiplier": "Toprak çarpanı",
    "Gravel multiplier": "Çakıl çarpanı",
    "Softer brake on loose surfaces, firmer on tarmac.":
        "Gevşek yüzeylerde daha yumuşak fren, asfaltta daha sert.",
    "1.0 = unchanged. Scales final resistance force.":
        "1.0 = değişmez. Son direnç kuvvetini ölçekler.",
    "Lower = softer brake on dirt. Default 0.5.":
        "Düşük = toprakta daha yumuşak fren. Varsayılan 0.5.",
    "Lower = softer brake on gravel/water. Default 0.25.":
        "Düşük = çakıl/suda daha yumuşak fren. Varsayılan 0.25.",
    "Turbo lag": "Turbo gecikmesi",
    "Turbo lag vibration": "Turbo gecikme titreşimi",
    "Rumble speed (Hz)": "Gürültü hızı (Hz)",
    "Rumble strength": "Gürültü gücü",
    "Boost change sensitivity": "Boost değişim hassasiyeti",
    "Brief R2 rumble when boost pressure climbs.":
        "Boost basıncı yükselirken kısa R2 gürültüsü.",
    "Deep rumble frequency. Default 8.":
        "Derin gürültü frekansı. Varsayılan 8.",
    "Max vibration amplitude. Default 40.":
        "Maks titreşim genliği. Varsayılan 40.",
    "Min boost delta per tick to trigger. Default 0.05.":
        "Tetiklemek için tick başına min boost deltası. Varsayılan 0.05.",
    "Cooldown (ms)": "Bekleme (ms)",
    "Min gap between rumbles. Suppresses steady-state jitter. Default 300.":
        "Gürültüler arası min boşluk. Kararlı durum titremesini bastırır. Varsayılan 300.",
}
