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

    # --- вкладка «Настройки» — кнопки / подсказки ---
    "Reset to defaults": "Сбросить по умолчанию",
    "Click again to confirm reset": "Нажмите ещё раз для подтверждения сброса",
    "In Forza HUD: host 127.0.0.1 (try ::1 if it fails).":
        "В Forza HUD: host 127.0.0.1 (если не работает, попробуйте ::1).",
    "UDP port {port} is in use. Close the other listener or change the port in the System tab.": (
        "UDP-порт {port} уже занят. Закройте программу, которая его использует, "
        "или измените порт на вкладке «Система»."
    ),

    # --- вкладка «Система» — разделы / поля ---
    "Telemetry (applies on next launch)": "Телеметрия (применится при следующем запуске)",
    "Startup pulse": "Импульс при запуске",
    "Reconnect": "Переподключение",
    "Game detection": "Определение игры",
    "UDP port": "UDP-порт",
    "Startup buzz strength": "Сила вибрации при запуске",
    "Auto-reconnect when controller drops": "Автопереподключение при отключении геймпада",
    "Reconnect check interval (s)": "Интервал проверки подключения (с)",
    "Auto-exit when the game closes": "Автовыход при закрытии игры",
    "Game-watch check interval (s)": "Интервал проверки игры (с)",

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
    "Speed-based throttle": "Зависимость газа от скорости",
    "Extra force at standstill": "Доп. усилие на месте",
    "Fade-out speed (km/h)": "Скорость затухания (км/ч)",
    "Extra resistance at low speed for precise control, lighter at high speed.":
        "Доп. сопротивление на низкой скорости для точного контроля, легче на высокой.",
    "0 = off. Flat resistance added at 0 km/h, fading to normal.":
        "0 = выкл. Плоское сопротивление при 0 км/ч, затухая до нормы.",
    "Speed where boost fully fades. Default 80.":
        "Скорость, где усиление полностью затухает. По умолчанию 80.",
    "Surface brake resistance": "Поверхностное торможение",
    "Tarmac multiplier": "Множитель асфальта",
    "Dirt multiplier": "Множитель грязи",
    "Gravel multiplier": "Множитель гравия",
    "Softer brake on loose surfaces, firmer on tarmac.":
        "Мягкий тормоз на рыхлых поверхностях, жёсткий на асфальте.",
    "1.0 = unchanged. Scales final resistance force.":
        "1.0 = без изменений. Масштабирует итоговое сопротивление.",
    "Lower = softer brake on dirt. Default 0.5.":
        "Ниже = мягче тормоз на грязи. По умолчанию 0.5.",
    "Lower = softer brake on gravel/water. Default 0.25.":
        "Ниже = мягче тормоз на гравии/воде. По умолчанию 0.25.",
    "Turbo lag": "Турбояма",
    "Turbo lag vibration": "Вибрация турбоямы",
    "Rumble speed (Hz)": "Скорость гула (Гц)",
    "Rumble strength": "Сила гула",
    "Boost change sensitivity": "Чувствительность изменения буста",
    "Brief R2 rumble when boost pressure climbs.":
        "Краткая вибрация R2 при росте давления наддува.",
    "Deep rumble frequency. Default 8.":
        "Глубокая частота гула. По умолчанию 8.",
    "Max vibration amplitude. Default 40.":
        "Макс. амплитуда вибрации. По умолчанию 40.",
    "Min boost delta per tick to trigger. Default 0.15.":
        "Мин. дельта буста за тик для срабатывания. По умолчанию 0.15.",
    "Cooldown (ms)": "Перезарядка (мс)",
    "Min gap between rumbles. Suppresses steady-state jitter. Default 300.":
        "Мин. пауза между вибрациями. Подавляет дрожание. По умолчанию 300.",
}
