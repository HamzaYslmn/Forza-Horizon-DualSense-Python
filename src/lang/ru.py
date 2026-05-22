# -*- coding: utf-8 -*-

"""Русский каталог перевода. Ключи — английские исходные строки."""

NAME = "Русский"

STRINGS = {
    # ============================================================
    # Верхняя панель / общее
    # ============================================================

    "Profile: {name}": "Профиль: {name}",
    "Active: {name}": "Активен: {name}",
    "Default": "По умолчанию",

    "DualSense": "DualSense",
    "connected": "подключен",
    "waiting": "ожидание",
    "active": "активен",
    "(none)": "(нет)",

    "Controls": "Управление",
    "Profiles": "Профили",
    "Settings": "Настройки",
    "System": "Система",
    "Language": "Язык",
    "Logs": "Логи",

    "Quit": "Выход",
    "Changelog": "Изменения",
    "♥ Sponsor": "♥ Поддержать",

    # ============================================================
    # Вкладка Управление
    # ============================================================

    "Shift thump": "Толчок при переключении",
    "ABS rumble": "Вибрация ABS",
    "Static brake wall": "Фиксированный упор тормоза",
    "Brake stiffness": "Жесткость тормоза",
    "Handbrake stiffness bonus": "Доп. жесткость ручника",

    "Redline buzz": "Вибрация на отсечке",
    "Wheelspin buzz": "Вибрация при пробуксовке",
    "Throttle stiffness": "Жесткость газа",

    # ============================================================
    # Вкладка Настройки — разделы
    # ============================================================

    "Pedals / deadzones": "Педали / мертвые зоны",
    "Pedal dead zones": "Мертвые зоны педалей",

    "Brake (left trigger)": "Тормоз (левый курок)",
    "Left trigger - Brake force": "Левый курок — усилие тормоза",

    "Brake static wall": "Фиксированный упор тормоза",
    "Left trigger - Static wall (optional)": "Левый курок — фиксированный упор",

    "Throttle (right trigger)": "Газ (правый курок)",
    "Right trigger - Gas force": "Правый курок — усилие газа",

    "ABS": "ABS",
    "ABS (anti-lock brake) rumble": "Вибрация ABS",

    "Rev limiter": "Ограничитель оборотов",
    "Redline (rev limiter) buzz": "Вибрация отсечки оборотов",

    "Gear shift thump": "Толчок при переключении передачи",

    # ============================================================
    # Вкладка Настройки — поля
    # ============================================================

    "Accel deadzone": "Мертвая зона газа",
    "Gas trigger dead zone": "Мертвая зона газа",

    "Brake deadzone": "Мертвая зона тормоза",
    "Brake trigger dead zone": "Мертвая зона тормоза",

    "Baseline force": "Базовое усилие",
    "Resting stiffness": "Начальная жесткость",

    "Max force": "Максимальное усилие",
    "Hard-press stiffness": "Жесткость при полном нажатии",

    "Curve": "Кривая",
    "Stiffness curve shape": "Форма кривой жесткости",

    "Handbrake bonus": "Бонус ручника",
    "Handbrake extra stiffness": "Доп. жесткость ручника",

    "Static wall at": "Позиция упора",
    "Wall position on the trigger": "Позиция упора на курке",

    "Static wall force": "Сила упора",
    "Wall hardness": "Жесткость упора",

    "Brake threshold": "Порог торможения",
    "Only when braking harder than": "Только при торможении сильнее",

    "Min speed (km/h)": "Мин. скорость (км/ч)",
    "Only when faster than (km/h)": "Только на скорости выше (км/ч)",

    "Slip ratio threshold": "Порог проскальзывания",
    "Wheel slip sensitivity": "Чувствительность к проскальзыванию колес",

    "Combined slip threshold": "Общий порог скольжения",
    "Tire grip sensitivity": "Чувствительность к потере сцепления",

    "Frequency (Hz)": "Частота (Гц)",
    "Rumble speed (Hz)": "Скорость вибрации (Гц)",
    "Buzz speed (Hz)": "Скорость жужжания (Гц)",
    "Thump speed (Hz)": "Скорость толчка (Гц)",

    "Amplitude": "Сила",
    "Rumble strength": "Сила вибрации",
    "Buzz strength": "Сила жужжания",
    "Thump strength": "Сила толчка",

    "Trigger at RPM ratio": "Срабатывание по оборотам",
    "Fire near redline at": "Срабатывать у отсечки на",

    "Hold (ms)": "Удержание (мс)",
    "Buzz hold time (ms)": "Длительность жужжания (мс)",

    "Duration (ms)": "Длительность (мс)",
    "Thump length (ms)": "Длительность толчка (мс)",

    # ============================================================
    # Кнопки / подсказки настроек
    # ============================================================

    "Reset to defaults": "Сбросить по умолчанию",
    "Click again to confirm reset": "Нажмите еще раз для подтверждения",

    "In Forza HUD: host 127.0.0.1 (try ::1 if it fails).": (
        "В Forza HUD: host 127.0.0.1. Если не работает, попробуйте ::1."
    ),

    "UDP port {port} is in use. Close the other listener or change the port in the System tab.": (
        "UDP-порт {port} уже используется. Закройте другую программу, "
        "которая его использует, или измените порт на вкладке «Система»."
    ),

    # ============================================================
    # Вкладка Система
    # ============================================================

    "Controller": "Геймпад",
    "Lock to controller": "Привязать к геймпаду",
    "Rescan": "Сканировать заново",

    "Auto (first found)": "Авто (первый найденный)",
    "attached now": "подключен сейчас",
    "(no serial - not selectable)": "(нет серийного номера — нельзя выбрать)",

    "Updates": "Обновления",
    "Check for updates at launch": "Проверять обновления при запуске",

    "Telemetry (applies on next launch)": "Телеметрия (применится при следующем запуске)",
    "UDP port": "UDP-порт",

    "Startup pulse": "Импульс при запуске",
    "Startup pulse force": "Сила импульса при запуске",
    "Startup buzz strength": "Сила вибрации при запуске",

    "Reconnect": "Переподключение",
    "Auto-reconnect controller (disable for HidHide)": (
        "Автопереподключение геймпада (отключить для HidHide)"
    ),
    "Auto-reconnect when controller drops": (
        "Автопереподключение при отключении геймпада"
    ),
    "Reconnect interval (s)": "Интервал переподключения (с)",
    "Reconnect check interval (s)": "Интервал проверки подключения (с)",

    "Game detection": "Определение игры",
    "Detect game (auto-exit when it closes)": (
        "Определять игру (автовыход при закрытии)"
    ),
    "Auto-exit when the game closes": "Автовыход при закрытии игры",
    "Poll interval (s)": "Интервал проверки (с)",
    "Game-watch check interval (s)": "Интервал проверки игры (с)",

    "When off, ZUV will not prompt for updates on startup. Toggle on and restart the app to check for a new release.": (
        "Если выключено, ZUV не будет предлагать обновления при запуске. "
        "Включите и перезапустите приложение, чтобы проверить новую версию."
    ),

    "ZUV not found: this build is not running inside a ZUV bundle (ZUV_CACHE_ROOT env var is missing), so the update toggle has nothing to control. Run the bundled .zuv.py to manage updates.": (
        "ZUV не найден: эта сборка запущена не внутри ZUV-пакета "
        "(переменная окружения ZUV_CACHE_ROOT отсутствует), поэтому переключатель "
        "обновлений ничего не контролирует. Запустите .zuv.py из поставки "
        "для управления обновлениями."
    ),

    # ============================================================
    # Вкладка Профили
    # ============================================================

    "Load": "Загрузить",
    "Rename": "Переименовать",
    "Delete": "Удалить",
    "Save": "Сохранить",

    "New profile name": "Новое имя профиля",
    "File: {path}": "Файл: {path}",

    "Note: the [b]Default[/] profile is reset to built-in values every time the app launches so new features and tuning come through. System settings (System tab) are preserved. To keep your own tuning across launches, save it as a named profile here.": (
        "Примечание: профиль [b]Default[/] сбрасывается к встроенным значениям "
        "при каждом запуске приложения, чтобы применялись новые функции и настройки. "
        "Системные настройки на вкладке «Система» сохраняются. Чтобы сохранить свои "
        "настройки между запусками, сохраните их здесь как отдельный профиль."
    ),

    # ============================================================
    # Вкладка Язык
    # ============================================================

    "Pick a language, then restart the app to apply it.": (
        "Выберите язык, затем перезапустите приложение, чтобы применить его."
    ),

    "Restart the app to apply the new language.": (
        "Перезапустите приложение, чтобы применить новый язык."
    ),

    # ============================================================
    # Вкладка Логи
    # ============================================================

    "level": "уровень",
    "pause": "пауза",
    "resume": "продолжить",
    "clear": "очистить",

    # ============================================================
    # Ошибки / статусы
    # ============================================================

    "Backend failed: {error}": "Ошибка запуска backend: {error}",
}