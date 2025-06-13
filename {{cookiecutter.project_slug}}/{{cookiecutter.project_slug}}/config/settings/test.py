"""
Test settings for DTD project.
"""

from .base import *

# Test database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable migrations during tests for speed
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Use fast password hasher for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Email backend for testing
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Media files for testing
MEDIA_ROOT = BASE_DIR / "test_media"

# Celery configuration for testing
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Disable debug toolbar in tests
DEBUG_TOOLBAR = False

# Test-specific settings
SECRET_KEY = "test-secret-key"
DEBUG = False

# Disable Turnstile in tests
TESTING = True
TURNSTILE_SITE_KEY = ""
TURNSTILE_SECRET_KEY = ""