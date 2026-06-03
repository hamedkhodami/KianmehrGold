import os

from .base import BASE_DIR

# ----------------------------------------------------------------


# --DATABASES-----------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.getenv("SQLITE_PATH", BASE_DIR.parent / "db.sqlite3"),
    }
}
# ----------------------------------------------------------------


# ---Static files-------------------------------------------------
STATICFILES_DIRS = [
    BASE_DIR / os.getenv("STATICFILES_DIRS", "static/assets"),
]
# ----------------------------------------------------------------
