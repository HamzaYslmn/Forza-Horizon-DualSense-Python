# -*- coding: utf-8 -*-
"""French (Français) catalog. Keys are the English source strings."""

NAME = "Français"

STRINGS = {
    # --- chrome / tabs ---
    "Controls": "Commandes",
    "Profiles": "Profils",
    "Settings": "Paramètres",
    "System": "Système",
    "Language": "Langue",
    "Logs": "Journaux",
    "Quit": "Quitter",
    "♥ Sponsor": "♥ Soutenir",
    "Changelog": "Notes de version",
    "connected": "connecté",
    "waiting": "en attente",
    "active": "actif",
    "(none)": "(aucun)",
    "Backend failed: {error}": "Le backend n'a pas démarré: {error}",
    "Profile: {name}": "Profil: {name}",
    "Active: {name}": "Actif: {name}",

    # --- controls tab (per-trigger effect switches) ---
    "Shift thump": "Coup de passage de vitesse",
    "ABS rumble": "Vibration ABS",
    "Static brake wall": "Mur de freinage fixe",
    "Brake stiffness": "Résistance du frein",
    "Handbrake stiffness bonus": "Bonus de résistance du frein à main",
    "Redline buzz": "Vibration de rupteur",
    "Wheelspin buzz": "Vibration de patinage",
    "Idle buzz": "Vibration au ralenti",
    "Throttle stiffness": "Résistance de l'accélérateur",

    # --- settings tab sections ---
    "Pedal dead zones": "Zones mortes des pédales",
    "Left trigger - Brake force": "Gâchette gauche - Force de freinage",
    "Left trigger - Static wall (optional)": "Gâchette gauche - Mur fixe (facultatif)",
    "Right trigger - Gas force": "Gâchette droite - Force d'accélération",
    "ABS (anti-lock brake) rumble": "Vibration ABS (antiblocage des freins)",
    "Redline (rev limiter) buzz": "Vibration de rupteur (limiteur de régime)",
    "Wheelspin buzz": "Vibration de patinage",
    "Idle buzz": "Vibration au ralenti",
    "Gear shift thump": "Coup de passage de vitesse",

    # --- settings tab fields ---
    "Gas trigger dead zone": "Zone morte de la gâchette d'accélération",
    "Brake trigger dead zone": "Zone morte de la gâchette de frein",
    "Resting stiffness": "Résistance au repos",
    "Hard-press stiffness": "Résistance en appui fort",
    "Stiffness curve shape": "Forme de la courbe de résistance",
    "Handbrake extra stiffness": "Résistance supplémentaire du frein à main",
    "Wall position on the trigger": "Position du mur sur la gâchette",
    "Wall hardness": "Dureté du mur",
    "Only when braking harder than": "Seulement si le freinage dépasse",
    "Only when faster than (km/h)": "Seulement si la vitesse dépasse (km/h)",
    "Wheel slip sensitivity": "Sensibilité au glissement des roues",
    "Tire grip sensitivity": "Sensibilité à l'adhérence des pneus",
    "Rumble speed (Hz)": "Vitesse de vibration (Hz)",
    "Rumble strength": "Intensité de vibration",
    "Fire near redline at": "Déclencher près du rupteur à",
    "Buzz speed (Hz)": "Vitesse de vibration (Hz)",
    "Buzz strength": "Intensité de vibration",
    "Buzz hold time (ms)": "Durée de maintien de la vibration (ms)",
    "Idle strength": "Intensité au ralenti",
    "Thump speed (Hz)": "Vitesse du coup (Hz)",
    "Thump strength": "Intensité du coup",
    "Thump length (ms)": "Durée du coup (ms)",

    # --- settings tab buttons / hints ---
    "Reset to defaults": "Rétablir les valeurs par défaut",
    "Click again to confirm reset": "Cliquez encore pour confirmer la réinitialisation",
    "In Forza HUD: host 127.0.0.1 (try ::1 if it fails).":
        "Dans le HUD Forza: hôte 127.0.0.1 (essayez ::1 si ça échoue).",
    "UDP port {port} is in use. Close the other listener or change the port in the System tab.":
        "Le port UDP {port} est déjà utilisé. Fermez l'autre écouteur ou changez le port dans l'onglet Système.",

    # --- system tab sections / fields ---
    "Telemetry (applies on next launch)": "Télémétrie (s'applique au prochain lancement)",
    "Startup pulse": "Vibration au démarrage",
    "Reconnect": "Reconnexion",
    "Game detection": "Détection du jeu",
    "UDP port": "Port UDP",
    "Startup buzz strength": "Intensité de vibration au démarrage",
    "Auto-reconnect when controller drops": "Reconnexion auto si la manette se déconnecte",
    "Reconnect check interval (s)": "Intervalle de vérification de reconnexion (s)",
    "Auto-exit when the game closes": "Quitter automatiquement quand le jeu se ferme",
    "Game-watch check interval (s)": "Intervalle de surveillance du jeu (s)",

    # --- system tab controller block ---
    "Controller": "Manette",
    "Lock to controller": "Verrouiller sur la manette",
    "Rescan": "Rechercher",
    "Auto (first found)": "Auto (première trouvée)",
    "attached now": "connectée maintenant",
    "(no serial - not selectable)": "(pas de numéro de série - non sélectionnable)",

    # --- system tab updates block ---
    "Updates": "Mises à jour",
    "Check for updates at launch": "Vérifier les mises à jour au lancement",
    "When off, ZUV will not prompt for updates on startup. Toggle on and restart the app to check for a new release.":
        "Quand il est désactivé, ZUV ne proposera pas de mise à jour au démarrage. Activez l'option et redémarrez l'application pour vérifier s'il existe une nouvelle version.",
    "ZUV not found: this build is not running inside a ZUV bundle (ZUV_CACHE_ROOT env var is missing), so the update toggle has nothing to control. Run the bundled .zuv.py to manage updates.":
        "ZUV introuvable: cette version ne tourne pas dans un paquet ZUV (la variable d'environnement ZUV_CACHE_ROOT est manquante), donc l'option de mise à jour n'a rien à contrôler. Lancez le fichier .zuv.py empaqueté pour gérer les mises à jour.",

    # --- profiles tab ---
    "Load": "Charger",
    "Rename": "Renommer",
    "Delete": "Supprimer",
    "Save": "Enregistrer",
    "New profile name": "Nom du nouveau profil",
    "File: {path}": "Fichier: {path}",
    "Note: the [b]Default[/] profile is reset to built-in values every time the app launches so new features and tuning come through. System settings (System tab) are preserved. To keep your own tuning across launches, save it as a named profile here.":
        "Remarque: le profil [b]Default[/] est rétabli aux valeurs intégrées à chaque lancement de l'application afin que les nouvelles fonctions et les réglages arrivent bien. Les paramètres système (onglet Système) sont conservés. Pour garder vos propres réglages entre les lancements, enregistrez-les ici dans un profil nommé.",

    # --- logs tab ---
    "level": "niveau",
    "pause": "pause",
    "resume": "reprendre",
    "clear": "effacer",

    # --- language tab ---
    "Pick a language, then restart the app to apply it.":
        "Choisissez une langue, puis redémarrez l'application pour l'appliquer.",
    "Restart the app to apply the new language.":
        "Redémarrez l'application pour appliquer la nouvelle langue.",
}
