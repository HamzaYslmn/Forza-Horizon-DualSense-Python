<p align="right">
  <a href="../README.md">English</a> •
  <strong>Türkçe</strong> •
  <a href="ReadmeJA.md">日本語</a> •
  <a href="ReadmeZH.md">简体中文</a>
</p>

<div align="center">
  <h1>🏎️ Forza Horizon - DualSense Adaptive Triggers</h1>
  <p><strong>PC'de Forza Horizon için gerçek tetik tepkisi.</strong></p>
  <p><em>Frenleri hisset. Motoru hisset. Kurulum karmaşası yok.</em></p>
</div>

> Steam profilim: <https://steamcommunity.com/id/teccno/>
> 
> CS:GO eşyası ile destek olmak için :D : <https://steamcommunity.com/tradeoffer/new/?partner=291638630&token=Xyg4vITU>

<div align="center">
  <a href="https://www.youtube.com/watch?v=-3Cp0PfL52Y">
    <img src="img/tuiyoutube.png" alt="Forza Horizon DualSense Adaptive Trigger Mod" style="width:100%;">
  </a>
</div>

> 💛 Bu projenin ilerlemesini sağlamak için bana Forza Horizon 6 hediye ederek sponsor olan **[Jared (jmac122)](https://github.com/jmac122)**'e çok teşekkürler.

---

## 📜 İçindekiler
1. [Ne işe yarar](#-ne-işe-yarar)
2. [Kurulum](#-kurulum)
3. [Oyun içi kurulum](#-oyun-içi-kurulum)
4. [Steam Haptics'i Etkinleştirme](#-steam-hapticsi-etkinleştirme)
5. [Çalıştırın](#-çalıştırın)
6. [Steam ile Otomatik Başlatma](#-steam-ile-otomatik-başlatma)
7. [Hissi Ayarlama](#-hissi-ayarlama)
8. [Sorun Giderme](#-sorun-giderme)
9. [Teşekkürler](#-teşekkürler)

---

## 💡 Ne işe yarar

Forza Horizon araba telemetrisini UDP üzerinden gönderir, ancak Steam Input DualSense'in **adaptif tetiklerini** kullanmaz. Bu küçük uygulama aradaki boşluğu doldurur:

- **Sol tetik (fren)** - bastıkça daha sert itme uygular. Lastikler kaydığında ABS gibi titrer. El freni çekildiğinde ekstra direnç gösterir.
- **Sağ tetik (gaz)** - yumuşak kademeli direnç. Vites geçişlerinde vuruntu (darbe) hissi. Devir sınırında (rev limiter) titreme.

### Kumandanızla Steam ile çakışmadan nasıl konuşur?

```
┌──────────────────┐    UDP 5300     ┌──────────────────┐    HID write    ┌─────────────┐
│  Forza Horizon   │ ──────────────► │  Bu uygulama     │ ──────────────► │  DualSense  │
│  (Data Out)      │  telemetrisi    │  (sadece tetik   │  sadece tetik   │  kontrolcü  │
│  └───────────────┘  324 byte       │   bitleri)       │                 └─────────────┘
                                     └──────────────────┘                        ▲
                                                                                 │
                                     ┌──────────────────┐    HID write           │
                                     │  Steam Input     │ ──────────────────────►│
                                     │  (titreşim bitl.)│  titreşim + tuşlar     │
                                     └──────────────────┘
```

Hem uygulama hem de Steam aynı kontrolcüye yazar - ancak **farklı byte**'lara dokunurlar:

- Steam, **titreşim motorlarını** (rumble) ve tuş eşlemelerini yönetir.
- Bu uygulama ise yalnızca **adaptif tetik** bitlerini değiştirir (`valid_flag0` içindeki `0x04` ve `0x08` bitleri).
- HID cihazı **bloklamayan (non-blocking) modda** açılır, böylece yazma işlemleri kontrolcüyü beklemeden anında gerçekleşir. Sıraya girme veya Steam'i engelleme durumu olmaz.

Bu yüzden ikisini aynı anda çalıştırabilirsiniz ve hiçbir şey birbirini bozmaz.

---

## 🛠️ Kurulum

**Gereksinimler:** Windows 10/11 veya Linux ve bir DualSense kontrolcüsü (USB veya Bluetooth).

1. [En son sürüme (latest release)](https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python/releases/latest) gidin.
2. **`win_start.bat`** (Windows) veya **`linux_start.sh`** (Linux) dosyasını indirin.
3. Dosyayı boş bir klasöre koyun.
4. **Önemli:** Öncelikle **`uv`** aracını manuel olarak kurmanızı şiddetle tavsiye ederiz. PowerShell'i açıp şu komutu çalıştırın:
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
   - Bunu yapmazsanız, `win_start.bat` aracı `uv`'yi otomatik olarak kurmaya çalışacaktır. Ancak Windows, PowerShell'de "Execution Policy" (Çalıştırma Politikası) hatası vererek bu otomatik kurulumu engelleyebilir.
   - **Eğer Çalıştırma Politikası hatası alırsanız:** Klasörde **Shift + Sağ Tık** yapın, **"PowerShell penceresini burada açın"** seçeneğine tıklayın, `Set-ExecutionPolicy RemoteSigned -scope CurrentUser` yapıştırıp Enter'a basın, ardından `Y` yazıp tekrar Enter'a basın.
5. `win_start.bat` (veya `linux_start.sh`) dosyasına çift tıklayarak çalıştırın.

Başlatıcı (launcher) uygulamanın indirilmesini, ortamın hazırlanmasını ve çalıştırılmasını otomatik halleder. Sonraki açılışlarda güncellemeleri de denetler.

> [!NOTE]
> Her sürüme deneysel bir seçenek olarak ayrıca tek dosyalık bir **Windows `.exe`** de eklenmiştir. Uygulamayı çalıştırmanın **önerilen** yolu yine **`win_start.bat`**'tır — kendini günceller ve her Windows sürümünde aynı şekilde çalışır.

> **Linux ekstraları:** `libhidapi` paketini kurun (`sudo apt install libhidapi-hidraw0` / `sudo pacman -S hidapi` / `sudo dnf install hidapi`) ve `app/packaging/linux/70-dualsense.rules` dosyasındaki udev kuralını ekleyin. Ardından kontrolcüyü bir kez çıkarıp geri takın.

### 🎮 SISR ile Oynama (Xbox Uygulaması / Windows Mağazası kullanıcıları)

Oyunu Xbox Uygulaması veya Microsoft Store üzerinden oynuyorsanız, oyunun kontrolcünüzü Xbox kumandası olarak tanıması için bir araca ihtiyacınız olacak. Seçeneklerden biri **[SISR (Steam Input System Redirector)](https://github.com/Alia5/SISR)** — Steam Input'u sistem seviyesine yönlendirip gerçek bir Xbox kontrolcüsü taklit eder, böylece Windows Mağazası uygulamaları ve hile korumalı (anti-cheat) oyunlarda bile çalışır.

SISR kontrolcüyü **Steam Input** üzerinden yönlendirdiği için, Steam fiziksel DualSense'i özel olarak ele geçirip bu uygulamanın bağlanmasını engelleyebilir. Bunu önlemek için **programları tam olarak şu sırayla başlatmalısınız**:

1. **İlk olarak BU UYGULAMAYI başlatın** (`win_start.bat`) ve tetiklerdeki kısa titreşim sinyalini bekleyin.
2. **İkinci olarak SISR'ı (ve Steam'i) başlatın.**
3. **Son olarak Forza Horizon'ı başlatın.**

*(Not: Oyun esnasında kontrolcünüzün bağlantısı kesilirse, SISR'ı kapatın, bu uygulamayı yeniden başlatın ve ardından SISR'ı tekrar açın. SISR kurulumu ve taklit seçenekleri için [SISR README](https://github.com/Alia5/SISR) sayfasına bakın.)*

<details>
<summary>Manuel kurulum (geliştiriciler için)</summary>

```bash
git clone https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python
cd Forza-Horizon-DualSense-Python/src
uv sync
uv run main.py
```

`uv` kurmak için: `pip install uv` veya [astral.sh/uv](https://astral.sh/uv/).
</details>

---

## 🎯 Oyun içi kurulum

Forza Horizon'da, **Ayarlar → HUD ve Oynanış** (Settings → HUD and Gameplay) bölümünü açıp en alta kaydırın:

| Ayar | Değer |
|------|-------|
| Telemetriyi Etkinleştir (Data Out) | **AÇIK** (ON) |
| Telemetri IP Adresi | **127.0.0.1** |
| Telemetri Bağlantı Noktası | **5300** |

> [!NOTE]
> Bazı Forza sürümlerinde IP adresi olarak `127.0.0.1` yazmak çalışmayabilir. Eğer uygulama telemetri verisi almıyorsa, IP adresi yerine `::1` (IPv6 loopback) yazmayı deneyin.

<p align="center">
  <img src="img/en.png" alt="İngilizce Ayarlar" width="48%" style="border-radius: 8px;">
  &nbsp;
  <img src="img/tr.png" alt="Türkçe Ayarlar" width="48%" style="border-radius: 8px;">
</p>

---

## 🔊 Steam Haptics'i Etkinleştirme

**Steam**, DualSense kontrolcünüzdeki sol ve sağ titreşim motorlarını titretebilir. Bunları etkinleştirmek için:

### Steam Ayarları:
1. Kütüphanenizde **Forza Horizon**'a sağ tıklayın → **Özellikler**.
2. **Kontrolcü → Ek Ayarlar** bölümüne gidin.
3. **DualSense titreşimi** seçeneğinin **AÇIK** olduğundan emin olun.

### Oyun içi (Forza Horizon):
1. **Ayarlar → Gelişmiş Kontroller** bölümünü açın.
2. **Titreşim** seçeneğini bulun ve etkinleştirin.

### DualSense yazılımı:
En iyi sonuç için resmi **PlayStation® Aksesuarları** yazılımını kurun:
- İndir: [PlayStation® Aksesuarları](https://fwupdater.dl.playstation.net/fwupdater/PlayStationAccessoriesInstaller.exe)

Bu, Windows için DualSense belleniminizin güncel olmasını sağlar.

> ℹ️ **Adaptif Tetikler Hakkında:** Steam bu oyun için DualSense adaptif tetiklerini desteklemez. **Bu uygulamanın** yaptığı şey tam olarak budur - Steam'in sağladığı titreşimin (rumble) üzerine gerçekçi tetik geri bildirimlerini (fren direnci, motor tepkisi, ABS titreşimleri, vites darbeleri, devir sınırı uyarısı) ekler.

---

## ▶️ Çalıştırın

**`win_start.bat`** (Windows) veya **`linux_start.sh`** (Linux) dosyasına çift tıklayın.

Tetiklerde kısa bir titreşim hissedeceksiniz - bu çalıştığı anlamına gelir. Şimdi Forza Horizon'ı başlatıp sürmeye başlayabilirsiniz.

> Başlatıcıyı Forza Horizon'dan **önce** açın. Eğer HidHide kullanıyorsanız `python.exe` dosyasına izin verin (allowlist).

---

## 🎮 Steam ile Otomatik Başlatma

Oyuna başlarken tetiklerin otomatik açılmasını istiyorsanız, Steam'e önce bu başlatıcıyı çalıştırmasını söyleyebilirsiniz.
> ⚠️ **Uyarı:** Bu yöntemle otomatik başlatmak bazen uygulama ile ilgili sorunlara yol açabilir. En kararlı deneyim için, dosyaya çift tıklayarak manuel çalıştırmanız önerilir.

1. Steam'de, **Forza Horizon**'a sağ tıklayın → **Özellikler**.
2. **Genel** sekmesinde **Başlatma Seçenekleri**'ni bulun.
3. Tercihinize göre aşağıdaki komutlardan birini yapıştırın (`win_start.bat` dosyanızın gerçek yolunu yazmayı unutmayın):

   * **Seçenek A: Steam Arayüzü ve Oynama Süresi Takibini Korumak (Önerilen)**
     Bu seçenek, komutu `cmd.exe /c` ile sararak Steam'in süreci izlemesini sağlar, böylece **Steam Arayüzü (Shift+Tab)** ve **Oynama Süresi Takibi** aktif kalır ve konsol penceresi işlem bitince otomatik kapanır:
     ```text
     "C:\Windows\System32\cmd.exe" /c ""C:\Yolunuz\Forza-Horizon-DualSense-Python\win_start.bat" %command%"
     ```

   * **Seçenek B: Daha Basit Yöntem**
     Doğrudan çalıştırma yöntemi (Steam arayüzü ve oynama süresi takibi çalışmayabilir):
     ```text
     "C:\Yolunuz\Forza-Horizon-DualSense-Python\win_start.bat" %command%
     ```

Bu kadar. **Oyna** düğmesine bastığınızda önce başlatıcı çalışır, ardından oyun açılır.

![Steam başlatma seçenekleri](img/steaming.png)

<details>
<summary>Gelişmiş - Python betiğini doğrudan çalıştırma (BAT dosyası olmadan)</summary>

Eğer repoyu klonladıysanız ve `uv` kullanıyorsanız, **Başlatma Seçenekleri**'ne şunu yapıştırın:

```text
cmd /c "start /MIN /D C:\Yolunuz\Forza-Horizon-DualSense-Python\src uv run main.py" && %command%
```
</details>

---

## 🎚️ Hissi Ayarlama

Her efekt (fren gücü, ABS titreşimi, vites darbesi, devir sınırlayıcı vb.) dosya düzenlemeye gerek kalmadan **uygulama içerisindeki Ayarlar sayfasından** ayarlanabilir veya kapatılabilir. Değişiklikler bir sonraki açılışta geçerli olur.

> ⚠️ Devir sınırlandırma efekti sabit bir RPM değerine göre değil, `rpm / max_rpm` oranına göre tetiklenir. Farklı arabalar farklı oranlarda devir sınırına ulaştığından araba bazlı ufak ayarlamalar gerekebilir.

---

## 🩺 Sorun Giderme

| Belirti | Çözüm |
|---------|-------|
| `DualSense gamepad interface not found` | Kontrolcü bağlı değil ya da HidHide onu gizliyor - `python.exe` dosyasına izin verin. |
| `No UDP packets yet` | Forza'nın Data Out ayarı kapalı, IP/port yanlış, Windows Güvenlik Duvarı engelliyor ya da IP adresini `127.0.0.1` yerine `::1` yapmayı deneyin. |
| Windows Defender / SmartScreen `win_start.bat` dosyasını engelliyor | 1. Mavi "Windows bilgisayarınızı korudu" ekranında **"Ek bilgi"** seçeneğine tıklayın.<br>2. Altta çıkan **"Yine de çalıştır"** butonuna basın. (Betik yalnızca gerekli bağımlılıkları indirir.) |
| Tetikler çok güçsüz | `brake_max_force` / `throttle_max_force` değerini yükseltin veya ilgili `curve` değerini düşürün. |
| Tetikler duvar gibi çok sert | `brake_max_force` / `throttle_max_force` değerini düşürün veya ilgili `curve` değerini yükseltin. |
| Tetikler hafif basışta bile çok sert | Başlangıç gücünü (baseline force) düşürün veya `curve` değerini yükseltin. |
| Vites geçişlerinde titreşim yok | Araba 3 km/s hızdan hızlı gitmeli ve geçerli vitesler arasında geçiş yapmalıdır. |
| Açılış titreşiminden sonra konsol ekranı boş kalıyor | TUI arayüzünü atlamak için terminalden `cd src && uv run main.py --headless` komutu ile çalıştırın. |

---

## 📁 Proje Yapısı

```
src/
├── main.py                          # Giriş noktası
└── modules/
    ├── settings.py                  # 👈 düzenleyeceğiniz dosya
    ├── dualsense/
    │   ├── main.py                              # HID katmanı
    │   └── adaptive_trigger.py                 # genel efekt ilkelleri
    └── forzahorizon/
        ├── udp_listener.py                     # UDP ayrıştırıcı
        └── effects.py                          # Forza'ya özel Controller + animasyonlar
```

---

## 🙏 Teşekkürler

**[HamzaYslmn](https://github.com/HamzaYslmn)** tarafından geliştirildi.

### 💛 Sponsorlar

- **[Jared (jmac122)](https://github.com/jmac122)** - bu projenin devam edebilmesi için bana Forza Horizon 6 hediye etti. Teşekkürler Jared!
- **[BeaudinSan](https://github.com/BeaudinSan)** - inanılmaz cömert desteğiniz için çok teşekkür ederim! Benim için gerçekten çok değerli.
- **[McLarenF1God](https://github.com/McLarenF1God)** - Forza Horizon 6 DLC'leri için teşekkürler!
- **[PlusMinusZer0](https://github.com/PlusMinusZer0)** - Puding için teşekkürler!
- **[dotcom](https://github.com/a0938670973-dotcom)** - Kek için teşekkürler!
- **[wallbangz](https://github.com/wallbangz)** - Kek için teşekkürler!
- **[BambinoPinguino](https://github.com/BambinoPinguino)** - Çay için teşekkürler!
- **[Ereldun](https://steamcommunity.com/)** - Kahve için teşekkürler!
- **[Clevens克林](https://steamcommunity.com/)** - Şeker için teşekkürler!

---
*Daha sürükleyici bir yarış deneyimi için geliştirildi*
