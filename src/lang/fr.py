# -*- coding: utf-8 -*-
"""Français (French) catalog. Keys are the English source strings."""

NAME = "Français"

STRINGS = {
    # --- chrome / tabs ---
    "Controls": "Contrôles",
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
    "Backend failed: {error}": "Échec du backend : {error}",
    "Profile: {name}": "Profil : {name}",
    "Active: {name}": "Actif : {name}",

    # --- settings tab sections ---
    "Pedal dead zones": "Zones mortes des pédales",
    "Left trigger - Brake force": "Gâchette gauche - Force de freinage",
    "Left trigger - Static wall (optional)": "Gâchette gauche - Mur statique (optionnel)",
    "Right trigger - Gas force": "Gâchette droite - Force d'accélération",
    "ABS (anti-lock brake) rumble": "Vibration ABS (antiblocage)",
    "Redline (rev limiter) buzz": "Vibration zone rouge (limiteur de régime)",
    "Wheelspin buzz": "Vibration patinage roues",
    "Gear shift thump": "Choc de changement de vitesse",

    # --- settings tab fields ---
    "Gas trigger dead zone": "Zone morte gâchette accélérateur",
    "Brake trigger dead zone": "Zone morte gâchette frein",
    "Resting stiffness": "Résistance au repos",
    "Hard-press stiffness": "Résistance en appui franc",
    "Stiffness curve shape": "Forme de la courbe de résistance",
    "Handbrake extra stiffness": "Résistance supplémentaire frein à main",
    "Wall position on the trigger": "Position du mur sur la gâchette",
    "Wall hardness": "Dureté du mur",
    "Only when braking harder than": "Seulement en freinant plus fort que",
    "Only when faster than (km/h)": "Seulement au-dessus de (km/h)",
    "Wheel slip sensitivity": "Sensibilité au glissement des roues",
    "Tire grip sensitivity": "Sensibilité à l'adhérence des pneus",
    "Rumble speed (Hz)": "Vitesse de vibration (Hz)",
    "Rumble strength": "Intensité de vibration",
    "Fire near redline at": "Déclencher près de la zone rouge à",
    "Buzz speed (Hz)": "Vitesse du buzz (Hz)",
    "Buzz strength": "Intensité du buzz",
    "Buzz hold time (ms)": "Durée du buzz (ms)",
    "Thump speed (Hz)": "Vitesse du choc (Hz)",
    "Thump strength": "Intensité du choc",
    "Thump length (ms)": "Durée du choc (ms)",

    # --- settings tab buttons / hints ---
    "Reset to defaults": "Réinitialiser les valeurs par défaut",
    "Click again to confirm reset": "Cliquer à nouveau pour confirmer",
    "In Forza HUD: host 127.0.0.1 (try ::1 if it fails).":
        "Dans Forza HUD : host 127.0.0.1 (essayer ::1 si ça ne marche pas).",
    "UDP port {port} is in use. Close the other listener or change the port in the System tab.":
        "Le port UDP {port} est déjà utilisé. Fermer l'autre programme ou changer le port dans l'onglet Système.",

    # --- system tab sections / fields ---
    "Telemetry (applies on next launch)": "Télémétrie (appliqué au prochain lancement)",
    "Startup pulse": "Vibration au démarrage",
    "Reconnect": "Reconnexion",
    "Game detection": "Détection du jeu",
    "UDP port": "Port UDP",
    "Startup buzz strength": "Intensité de la vibration de démarrage",
    "Auto-reconnect when controller drops": "Reconnecter automatiquement si la manette se déconnecte",
    "Reconnect check interval (s)": "Intervalle de vérification reconnexion (s)",
    "Auto-exit when the game closes": "Quitter automatiquement quand le jeu se ferme",
    "Game-watch check interval (s)": "Intervalle de surveillance du jeu (s)",

    # --- system tab controller block ---
    "Controller": "Manette",
    "Lock to controller": "Verrouiller sur une manette",
    "Rescan": "Rescanner",
    "Auto (first found)": "Auto (première trouvée)",
    "attached now": "connectée actuellement",
    "(no serial - not selectable)": "(pas de numéro de série - non sélectionnable)",

    # --- system tab updates block ---
    "Updates": "Mises à jour",
    "Check for updates at launch": "Vérifier les mises à jour au lancement",
    "When off, ZUV will not prompt for updates on startup. Toggle on and restart the app to check for a new release.":
        "Désactivé, ZUV ne proposera pas de mise à jour au démarrage. Activer et redémarrer l'application pour vérifier une nouvelle version.",
    "ZUV not found: this build is not running inside a ZUV bundle (ZUV_CACHE_ROOT env var is missing), so the update toggle has nothing to control. Run the bundled .zuv.py to manage updates.":
        "ZUV introuvable : cette version ne s'exécute pas dans un paquet ZUV (variable d'environnement ZUV_CACHE_ROOT absente), le bouton de mise à jour n'a rien à contrôler. Lancer le fichier .zuv.py inclus pour gérer les mises à jour.",

    # --- system tab DSX block ---
    "DSX output": "Sortie DSX",
    "Use DSX instead of direct HID": "Utiliser DSX à la place du HID direct",
    "Requires DSX v3.1+ running. Takes effect on next launch.":
        "Nécessite DSX v3.1+ en cours d'exécution. Prend effet au prochain lancement.",
    "Auto-detect DSX port": "Détection automatique du port DSX",
    "Reads DSX_UDP_PortNumber.txt from %LOCALAPPDATA%\\DSX.":
        "Lit DSX_UDP_PortNumber.txt depuis %LOCALAPPDATA%\\DSX.",
    "DSX host": "Hôte DSX",
    "DSX port": "Port DSX",
    "Controller index": "Index du contrôleur",
    "DSX: checking...": "DSX : vérification...",
    "DSX: running": "DSX : actif",
    "DSX: not detected": "DSX : non détecté",
    "Refresh": "Actualiser",

    # --- profiles tab ---
    "Load": "Charger",
    "Rename": "Renommer",
    "Delete": "Supprimer",
    "Save": "Enregistrer",
    "New profile name": "Nom du nouveau profil",
    "File: {path}": "Fichier : {path}",
    "Note: the [b]Default[/] profile is reset to built-in values every time the app launches so new features and tuning come through. System settings (System tab) are preserved. To keep your own tuning across launches, save it as a named profile here.":
        "Note : le profil [b]Default[/] est réinitialisé aux valeurs par défaut à chaque lancement afin d'intégrer les nouvelles fonctionnalités et réglages. Les paramètres système (onglet Système) sont conservés. Pour garder vos réglages personnels entre les lancements, enregistrez-les ici sous un profil nommé.",

    # --- logs tab ---
    "level": "niveau",
    "pause": "pause",
    "resume": "reprendre",
    "clear": "effacer",

    # --- language tab ---
    "Pick a language, then restart the app to apply it.":
        "Choisir une langue, puis redémarrer l'application pour l'appliquer.",
    "Restart the app to apply the new language.":
        "Redémarrer l'application pour appliquer la nouvelle langue.",
}
