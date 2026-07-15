# -*- coding: utf-8 -*-
"""Deutsch (German) catalog. Keys are the English source strings."""

NAME = "Deutsch"

STRINGS = {
    # --- chrome / tabs ---
    "Controls": "Steuerung",
    "Profiles": "Profile",
    "Settings": "Einstellungen",
    "System": "System",
    "Language": "Sprache",
    "Logs": "Protokoll",
    "Quit": "Beenden",
    "♥ Sponsor": "♥ Sponsor",
    "Changelog": "Änderungsprotokoll",
    "connected": "verbunden",
    "waiting": "wartet",
    "active": "aktiv",
    "(none)": "(keine)",
    "Backend failed: {error}": "Backend fehlgeschlagen: {error}",
    "Profile: {name}": "Profil: {name}",
    "Active: {name}": "Aktiv: {name}",

    # --- controls tab (per-trigger effect switches) ---
    "Shift thump": "Schaltruck",
    "ABS rumble": "ABS-Vibration",
    "Static brake wall": "Statische Bremswand",
    "Brake stiffness": "Bremswiderstand",
    "Handbrake stiffness bonus": "Zusätzlicher Handbremswiderstand",
    "Redline buzz": "Drehzahlgrenze-Surren",
    "Wheelspin buzz": "Radschlupf-Surren",
    "Idle buzz": "Leerlauf-Surren",
    "Throttle stiffness": "Gaswiderstand",
    "LED Lighting": "LED-Beleuchtung",
    "LightBar": "RGB-Lichtleiste",
    "Player LED": "Spieler-LED",
    "ABS Light": "ABS-Anzeige",

    # --- settings tab sections ---
    "Pedal dead zones": "Pedal-Totzonen",
    "Left trigger - Brake force": "Linker Trigger - Bremskraft",
    "Left trigger - Static wall (optional)": "Linker Trigger - Statische Wand (optional)",
    "Right trigger - Gas force": "Rechter Trigger - Gaskraft",
    "ABS (anti-lock brake) rumble": "ABS (Antiblockiersystem)-Vibration",
    "Redline (rev limiter) buzz": "Drehzahlgrenze (Drehzahlbegrenzer)-Surren",
    "Wheelspin buzz": "Radschlupf-Surren",
    "Idle buzz": "Leerlauf-Surren",
    "Gear shift thump": "Schaltruck",
    "LED Shift Light": "LED-Schaltanzeige",

    # --- settings tab fields ---
    "Gas trigger dead zone": "Gas-Trigger-Totzone",
    "Brake trigger dead zone": "Brems-Trigger-Totzone",
    "Resting stiffness": "Ruhewiderstand",
    "Hard-press stiffness": "Widerstand bei vollem Druck",
    "Stiffness curve shape": "Form der Widerstandskurve",
    "Handbrake extra stiffness": "Zusätzlicher Handbremswiderstand",
    "Wall position on the trigger": "Wandposition am Trigger",
    "Wall hardness": "Wandhärte",
    "Only when braking harder than": "Nur beim Bremsen stärker als",
    "Only when faster than (km/h)": "Nur bei Geschwindigkeit über (km/h)",
    "Wheel slip sensitivity": "Radschlupf-Empfindlichkeit",
    "Tire grip sensitivity": "Reifengrip-Empfindlichkeit",
    "Rumble speed (Hz)": "Vibrationsfrequenz (Hz)",
    "Rumble strength": "Vibrationsstärke",
    "Fire near redline at": "Auslösen nahe Drehzahlgrenze bei",
    "Buzz speed (Hz)": "Surrfrequenz (Hz)",
    "Buzz strength": "Surrstärke",
    "Buzz hold time (ms)": "Surr-Haltezeit (ms)",
    "Idle strength": "Leerlaufstärke",
    "Thump speed (Hz)": "Ruckfrequenz (Hz)",
    "Thump strength": "Ruckstärke",
    "Thump length (ms)": "Ruckdauer (ms)",
    "Auto-detect true redline": "Echte Drehzahlgrenze automatisch erkennen",
    "Print detection debug info": "Debug-Info der Erkennung ausgeben",
    "Samples required to lock": "Erforderliche Samples zur Arretierung",
    "RPM clustering tolerance": "RPM-Cluster-Toleranz",
    "Green zone threshold": "Grüner Bereich Schwellenwert",
    "Orange zone threshold": "Oranger Bereich Schwellenwert",
    "Red zone threshold": "Roter Bereich Schwellenwert",
    "Flash threshold": "Blink-Schwellenwert",

    # --- settings tab buttons / hints ---
    "Reset to defaults": "Auf Standard zurücksetzen",
    "Click again to confirm reset": "Zum Bestätigen erneut klicken",
    "In Forza HUD: host 127.0.0.1 (try ::1 if it fails).":
        "Im Forza-HUD: Host 127.0.0.1 (bei Problemen ::1 versuchen).",
    "Forward telemetry": "Telemetrie weiterleiten",
    "Mirror every received packet to another app (e.g. SimHub) without taking the port from it.":
        "Spiegelt jedes empfangene Paket an eine andere App (z. B. SimHub), ohne ihr den Port wegzunehmen.",
    "Forward to": "Weiterleiten an",
    "host:port targets, comma-separated. Default 127.0.0.1:5301.":
        "host:port-Ziele, durch Komma getrennt. Standard 127.0.0.1:5301.",
    "UDP port {port} is in use. Close the other listener or change the port in the System tab.":
        "UDP-Port {port} ist belegt. Schließen Sie den anderen Listener oder ändern Sie den Port im System-Tab.",
    "Dynamically detects rev limiter instead of using dashboard max RPM.":
        "Erkennt den Drehzahlbegrenzer algorithmisch, anstatt die maximale Drehzahl vom Armaturenbrett zu verwenden.",
    "Outputs redline detection state changes to the console.":
        "Gibt Zustandsänderungen der Drehzahlgrenzen-Erkennung in der Konsole aus.",
    "Number of valid peaks needed to lock the true redline.":
        "Anzahl der gültigen Spitzen, die zum Arretieren der echten Drehzahlgrenze erforderlich sind.",
    "Max RPM difference to consider peaks as the same redline.":
        "Maximale RPM-Differenz, um Spitzen als dieselbe Drehzahlgrenze zu betrachten (Cluster-Toleranz).",

    # --- system tab sections / fields ---
    "Forza telemetry (applies on next launch)": "Forza-Telemetrie (wird beim nächsten Start übernommen)",
    "Startup pulse": "Start-Impuls",
    "Reconnect": "Wiederverbinden",
    "Game detection": "Spielerkennung",
    "UDP port": "UDP-Port",
    "Startup buzz strength": "Start-Surrstärke",
    "Auto-reconnect when controller drops": "Automatisch wiederverbinden bei Controller-Verlust",
    "Reconnect check interval (s)": "Prüfintervall für Wiederverbindung (s)",
    "Auto-exit when the game closes": "Automatisch beenden, wenn das Spiel schließt",
    "Game-watch check interval (s)": "Prüfintervall der Spielüberwachung (s)",

    # --- DSX ---
    "DSX": "DSX",
    "DSX integration": "DSX-Integration",
    "Send triggers to DualSenseX over UDP. Takes effect immediately.":
        "Trigger über UDP an DualSenseX senden. Wird sofort wirksam.",
    "DSX connection": "DSX-Verbindung",
    "Host": "Host",
    "Port": "Port",
    "Default 127.0.0.1. Match the host in DSX settings.":
        "Standard 127.0.0.1. Muss mit dem Host in den DSX-Einstellungen übereinstimmen.",
    "Default 6969. Match the port in DSX settings.":
        "Standard 6969. Muss mit dem Port in den DSX-Einstellungen übereinstimmen.",
    "DSX is active - controller managed by DSX. Disable DSX to select a controller here.":
        "DSX ist aktiv - Controller wird von DSX verwaltet. Deaktivieren Sie DSX, um hier einen Controller auszuwählen.",
    "DSX: active": "DSX: aktiv",
    "DSX: off": "DSX: aus",

    # --- system tab controller block ---
    "Controller": "Controller",
    "Lock to controller": "Auf Controller festlegen",
    "Rescan": "Neu suchen",
    "Auto (first found)": "Automatisch (erster gefundener)",
    "attached now": "jetzt verbunden",
    "(no serial - not selectable)": "(keine Seriennummer - nicht auswählbar)",

    # --- system tab updates block ---
    "Updates": "Updates",
    "Check for updates at launch": "Beim Start nach Updates suchen",
    "When off, ZUV will not prompt for updates on startup. Toggle on and restart the app to check for a new release.":
        "Wenn deaktiviert, fragt ZUV beim Start nicht nach Updates. Aktivieren Sie die Option und starten Sie die App neu, um nach einer neuen Version zu suchen.",
    "ZUV not found: this build is not running inside a ZUV bundle (ZUV_CACHE_ROOT env var is missing), so the update toggle has nothing to control. Run the bundled .zuv.py to manage updates.":
        "ZUV nicht gefunden: Dieser Build läuft nicht in einem ZUV-Bundle (Umgebungsvariable ZUV_CACHE_ROOT fehlt), daher steuert der Update-Schalter nichts. Führen Sie die gebündelte .zuv.py aus, um Updates zu verwalten.",

    # --- profiles tab ---
    "Load": "Laden",
    "Rename": "Umbenennen",
    "Delete": "Löschen",
    "Save": "Speichern",
    "New profile name": "Neuer Profilname",
    "File: {path}": "Datei: {path}",
    "Note: the [b]Default[/] profile is reset to built-in values every time the app launches so new features and tuning come through. System settings (System tab) are preserved. To keep your own tuning across launches, save it as a named profile here.":
        "Hinweis: Das Profil [b]Default[/] wird bei jedem Start auf die integrierten Werte zurückgesetzt, damit neue Funktionen und Abstimmungen übernommen werden. Die Systemeinstellungen (System-Tab) bleiben erhalten. Um Ihre eigene Abstimmung über Neustarts hinweg zu behalten, speichern Sie sie hier als benanntes Profil.",
    "Profile": "Profil",
    "Saved profiles": "Gespeicherte Profile",
    "Save current settings": "Aktuelle Einstellungen speichern",
    "Save profile": "Profil speichern",
    "Share profile": "Profil teilen",
    "Export & Copy": "Exportieren & Kopieren",
    "Import": "Importieren",
    "Export the selected profile as a short code (copied to your clipboard), or paste a code below and import it.":
        "Das ausgewählte Profil als Kurzcode exportieren (in die Zwischenablage kopiert) oder unten einen Code einfügen und importieren.",
    "Save and switch named snapshots of your settings.":
        "Benannte Schnappschüsse Ihrer Einstellungen speichern und wechseln.",
    "The Default profile resets on every launch to pick up new features and tuning. System tab settings are preserved. Save a named profile to keep your own tuning.":
        "Das Default-Profil wird bei jedem Start zurückgesetzt, um neue Funktionen und Abstimmungen zu übernehmen. Die Einstellungen im System-Tab bleiben erhalten. Speichern Sie ein benanntes Profil, um Ihre eigene Abstimmung zu behalten.",
    "No profile selected.": "Kein Profil ausgewählt.",
    "Copied {name} to clipboard.": "{name} in die Zwischenablage kopiert.",
    "Copy failed. Select the code and copy manually.": "Kopieren fehlgeschlagen. Markieren Sie den Code und kopieren Sie ihn manuell.",
    "Export failed.": "Export fehlgeschlagen.",
    "Paste a code first.": "Fügen Sie zuerst einen Code ein.",
    "Invalid share code.": "Ungültiger Freigabecode.",
    "Imported as {name}.": "Als {name} importiert.",

    # --- controls / system descriptions ---
    "Toggle individual trigger effects. Changes save instantly.":
        "Einzelne Trigger-Effekte umschalten. Änderungen werden sofort gespeichert.",
    "Lock the app to a specific DualSense, or let it pick the first one.":
        "Die App auf einen bestimmten DualSense festlegen oder den ersten gefundenen verwenden.",
    "UDP port {port} in use": "UDP-Port {port} belegt",

    # --- logs tab ---
    "Level": "Stufe",
    "level": "Stufe",
    "pause": "Pause",
    "resume": "Fortsetzen",
    "clear": "Leeren",
    "latched": "fixiert",
    "Live application output. Increase verbosity for debugging.":
        "Live-Ausgabe der App. Für die Fehlersuche die Ausführlichkeit erhöhen.",

    # --- language tab ---
    "Available languages": "Verfügbare Sprachen",
    "Pick a language, then restart the app to apply it.":
        "Wählen Sie eine Sprache und starten Sie die App neu, um sie zu übernehmen.",
    "Restart the app to apply your choice.":
        "Starten Sie die App neu, um Ihre Auswahl zu übernehmen.",
    "Restart the app to apply the new language.":
        "Starten Sie die App neu, um die neue Sprache zu übernehmen.",

    # --- external links ---
    "Sponsor": "Sponsor",
}
