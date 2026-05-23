"""Settings model plus its on-disk persistence (preferences + named profiles)."""
from . import paths, preferences, profiles
from .preferences import PreferencesError
from .settings import Settings

__all__ = ["Settings", "paths", "preferences", "profiles", "PreferencesError"]
