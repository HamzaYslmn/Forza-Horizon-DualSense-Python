"""Check the latest GitHub release and warn if the local install is behind."""
import json
import logging
import threading
import urllib.request
from pathlib import Path

log = logging.getLogger("fhds")

REPO = "HamzaYslmn/Forza-Horizon-DualSense-Python"
API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"
REPO_URL = f"https://github.com/{REPO}"
# Written by win_start.bat / linux_start.sh next to the app/ folder.
VERSION_FILE = Path(__file__).resolve().parents[2].parent / ".version"


def _local_version() -> str | None:
    try:
        return VERSION_FILE.read_text(encoding="utf-8").strip() or None
    except OSError:
        return None


def _check(timeout: float) -> None:
    try:
        req = urllib.request.Request(API_URL, headers={"User-Agent": "fhds"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            latest = json.loads(r.read().decode()).get("tag_name")
    except Exception as e:
        log.debug("Update check failed: %s", e)
        return
    if not latest:
        return
    current = _local_version()
    if current and current != latest:
        log.warning(
            "New release %s available (you have %s). Relaunch via win_start.bat / linux_start.sh to update. %s/releases/latest",
            latest, current, REPO_URL,
        )
    elif not current:
        log.info("Latest release: %s - %s/releases/latest", latest, REPO_URL)


def log_latest_commit_age(timeout: float = 3.0) -> None:
    """Fire-and-forget background check. Never blocks startup."""
    threading.Thread(target=_check, args=(timeout,), daemon=True).start()
