# -*- coding: utf-8 -*-
"""Русский каталог перевода. Ключи — английские исходные строки."""

NAME = "Русский"

STRINGS = {
    # --- верхняя панель / вкладки ---
    "Controls": "Управление",
    "Profiles": "Профили",
    "Settings": "Настройки",
    "System": "Система",
    "Language": "Язык",
    "Logs": "Логи",
    "Quit": "Выход",
    "♥ Sponsor": "♥ Поддержать",
    "Changelog": "История изменений",
    "connected": "подключён",
    "waiting": "ожидание",
    "active": "активен",
    "(none)": "(нет)",
    "Backend failed: {error}": "Не удалось запустить бэкенд: {error}",
    "Profile: {name}": "Профиль: {name}",
    "Active: {name}": "Активен: {name}",

    # --- вкладка «Управление» (переключатели эффектов) ---
    "Shift thump": "Толчок при переключении",
    "ABS rumble": "Вибрация ABS",
    "Static brake wall": "Фиксированный упор тормоза",
    "Brake stiffness": "Жёсткость тормоза",
    "Handbrake stiffness bonus": "Доп. жёсткость ручника",
    "Redline buzz": "Вибрация на отсечке",
    "Wheelspin buzz": "Вибрация при пробуксовке",
    "Idle buzz": "Вибрация на холостом ходу",
    "Throttle stiffness": "Жёсткость газа",
    "LED Lighting": "LED-подсветка",
    "LightBar": "RGB-световая полоса",
    "Player LED": "LED игрока",
    "ABS Light": "Индикатор ABS",

    # --- вкладка «Настройки» — разделы ---
    "Pedal dead zones": "Мёртвые зоны педалей",
    "Left trigger - Brake force": "Левый курок — усилие тормоза",
    "Left trigger - Static wall (optional)": "Левый курок — фиксированный упор (необязательно)",
    "Right trigger - Gas force": "Правый курок — усилие газа",
    "ABS (anti-lock brake) rumble": "Вибрация ABS (антиблокировочной системы)",
    "Redline (rev limiter) buzz": "Вибрация на отсечке (ограничителе оборотов)",
    "Wheelspin buzz": "Вибрация при пробуксовке",
    "Idle buzz": "Вибрация на холостом ходу",
    "Gear shift thump": "Толчок при переключении передачи",
    "LED Shift Light": "LED-индикация передач",

    # --- вкладка «Настройки» — поля ---
    "Gas trigger dead zone": "Мёртвая зона курка газа",
    "Brake trigger dead zone": "Мёртвая зона курка тормоза",
    "Resting stiffness": "Жёсткость в покое",
    "Hard-press stiffness": "Жёсткость при полном нажатии",
    "Stiffness curve shape": "Форма кривой жёсткости",
    "Handbrake extra stiffness": "Доп. жёсткость ручника",
    "Wall position on the trigger": "Положение упора на курке",
    "Wall hardness": "Жёсткость упора",
    "Only when braking harder than": "Только при торможении сильнее",
    "Only when faster than (km/h)": "Только на скорости выше (км/ч)",
    "Wheel slip sensitivity": "Чувствительность к проскальзыванию колёс",
    "Tire grip sensitivity": "Чувствительность к потере сцепления",
    "Rumble speed (Hz)": "Частота вибрации (Гц)",
    "Rumble strength": "Сила вибрации",
    "Fire near redline at": "Срабатывать у отсечки при",
    "Buzz speed (Hz)": "Частота вибрации (Гц)",
    "Buzz strength": "Сила вибрации",
    "Buzz hold time (ms)": "Длительность вибрации (мс)",
    "Idle strength": "Сила на холостом ходу",
    "Thump speed (Hz)": "Частота толчка (Гц)",
    "Thump strength": "Сила толчка",
    "Thump length (ms)": "Длительность толчка (мс)",
    "Auto-detect true redline": "Автоопределение отсечки",
    "Print detection debug info": "Вывод отладочной информации",
    "Samples required to lock": "Пиков для фиксации",
    "RPM clustering tolerance": "Допуск группировки RPM",
    "Green zone threshold": "Порог зелёной зоны",
    "Orange zone threshold": "Порог оранжевой зоны",
    "Red zone threshold": "Порог красной зоны",
    "Flash threshold": "Порог мигания",

    # --- вкладка «Настройки» — кнопки / подсказки ---
    "Reset to defaults": "Сбросить по умолчанию",
    "Click again to confirm reset": "Нажмите ещё раз для подтверждения сброса",
    "In Forza HUD: host 127.0.0.1 (try ::1 if it fails).":
        "В Forza HUD: host 127.0.0.1 (если не работает, попробуйте ::1).",
    "Forward telemetry": "Пересылка телеметрии",
    "Mirror every received packet to another app (e.g. SimHub) without taking the port from it.":
        "Зеркалирует каждый полученный пакет в другое приложение (например, SimHub), не занимая порт.",
    "Forward to": "Пересылать на",
    "host:port targets, comma-separated. Default 127.0.0.1:5301.":
        "Цели host:port через запятую. По умолчанию 127.0.0.1:5301.",
    "UDP port {port} is in use. Close the other listener or change the port in the System tab.": (
        "UDP-порт {port} уже занят. Закройте программу, которая его использует, "
        "или измените порт на вкладке «Система»."
    ),
    "Dynamically detects rev limiter instead of using dashboard max RPM.":
        "Gösterge panelindeki maksimum RPM yerine algoritma ile devir sınırlayıcıyı algılar.",
    "Outputs redline detection state changes to the console.":
        "Kırmızı çizgi algılama durum değişikliklerini konsola yazdırır.",
    "Number of valid peaks needed to lock the true redline.":
        "Gerçek kırmızı çizgiyi kilitlemek için gereken geçerli tepe noktası sayısı.",
    "Max RPM difference to consider peaks as the same redline.":
        "Tepe noktalarını aynı kırmızı çizgi olarak kabul etmek için maksimum RPM farkı (kümeleme toleransı).",

    # --- вкладка «Система» — разделы / поля ---
    "Forza telemetry (applies on next launch)": "Forza-телеметрия (применится при следующем запуске)",
    "Startup pulse": "Импульс при запуске",
    "Reconnect": "Переподключение",
    "Game detection": "Определение игры",
    "UDP port": "UDP-порт",
    "Startup buzz strength": "Сила вибрации при запуске",
    "Auto-reconnect when controller drops": "Автопереподключение при отключении геймпада",
    "Reconnect check interval (s)": "Интервал проверки подключения (с)",
    "Auto-exit when the game closes": "Автовыход при закрытии игры",
    "Game-watch check interval (s)": "Интервал проверки игры (с)",

    # --- DSX ---
    "DSX": "DSX",
    "DSX integration": "Интеграция с DSX",
    "Send triggers to DualSenseX over UDP. Takes effect immediately.":
        "Отправлять триггеры в DualSenseX через UDP. Вступает в силу немедленно.",
    "DSX connection": "Подключение DSX",
    "Host": "Хост",
    "Port": "Порт",
    "Default 127.0.0.1. Match the host in DSX settings.":
        "По умолчанию 127.0.0.1. Должно совпадать с хостом в настройках DSX.",
    "Default 6969. Match the port in DSX settings.":
        "По умолчанию 6969. Должно совпадать с портом в настройках DSX.",
    "DSX is active - controller managed by DSX. Disable DSX to select a controller here.":
        "DSX активен — геймпад управляется DSX. Отключите DSX, чтобы выбрать геймпад здесь.",
    "DSX: active": "DSX: активен",
    "DSX: off": "DSX: выкл",

    # --- вкладка «Система» — блок геймпада ---
    "Controller": "Геймпад",
    "Lock to controller": "Привязать к геймпаду",
    "Rescan": "Сканировать заново",
    "Auto (first found)": "Авто (первый найденный)",
    "attached now": "подключён сейчас",
    "(no serial - not selectable)": "(нет серийного номера — нельзя выбрать)",

    # --- вкладка «Система» — блок обновлений ---
    "Updates": "Обновления",
    "Check for updates at launch": "Проверять обновления при запуске",
    "When off, ZUV will not prompt for updates on startup. Toggle on and restart the app to check for a new release.": (
        "Если выключено, ZUV не будет предлагать обновления при запуске. "
        "Включите и перезапустите приложение, чтобы проверить новую версию."
    ),
    "ZUV not found: this build is not running inside a ZUV bundle (ZUV_CACHE_ROOT env var is missing), so the update toggle has nothing to control. Run the bundled .zuv.py to manage updates.": (
        "ZUV не найден: эта сборка запущена не внутри ZUV-пакета "
        "(переменная окружения ZUV_CACHE_ROOT отсутствует), поэтому переключателю "
        "обновлений нечем управлять. Запустите .zuv.py из поставки для управления обновлениями."
    ),

    # --- вкладка «Профили» ---
    "Load": "Загрузить",
    "Rename": "Переименовать",
    "Delete": "Удалить",
    "Save": "Сохранить",
    "New profile name": "Имя нового профиля",
    "File: {path}": "Файл: {path}",
    "Note: the [b]Default[/] profile is reset to built-in values every time the app launches so new features and tuning come through. System settings (System tab) are preserved. To keep your own tuning across launches, save it as a named profile here.": (
        "Примечание: профиль [b]Default[/] сбрасывается к встроенным значениям при каждом "
        "запуске приложения, чтобы применялись новые функции и настройки. Системные настройки "
        "(вкладка «Система») сохраняются. Чтобы сохранить свои настройки между запусками, "
        "сохраните их здесь как отдельный профиль."
    ),

    # --- вкладка «Логи» ---
    "level": "уровень",
    "pause": "пауза",
    "resume": "продолжить",
    "clear": "очистить",

    # --- вкладка «Язык» ---
    "Pick a language, then restart the app to apply it.":
        "Выберите язык, затем перезапустите приложение, чтобы применить его.",
    "Restart the app to apply the new language.":
        "Перезапустите приложение, чтобы применить новый язык.",
}
