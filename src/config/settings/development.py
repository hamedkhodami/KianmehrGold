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


# ---Django-q config-----------------------------------------------
Q_CLUSTER = {
    "name": "gold",
    "workers": int(os.getenv("Q_CLUSTER_WORKERS", 2)),
    "recycle": int(os.getenv("Q_CLUSTER_RECYCLE", 500)),
    "timeout": int(os.getenv("Q_CLUSTER_TIMEOUT", 60)),
    "retry": int(os.getenv("Q_CLUSTER_RETRY", 90)),
    "queue_limit": int(os.getenv("Q_CLUSTER_QUEUE_LIMIT", 50)),
    "save_limit": int(os.getenv("Q_CLUSTER_SAVE_LIMIT", 100)),
    "redis": {
        "host": os.getenv("REDIS_HOST", "localhost"),
        "port": int(os.getenv("REDIS_PORT", 6379)),
        "db": int(os.getenv("REDIS_DB", 0)),
    },
}
# ----------------------------------------------------------------


# ---Static files-------------------------------------------------
STATICFILES_DIRS = [
    BASE_DIR / os.getenv("STATICFILES_DIRS", "static/assets"),
]
# ----------------------------------------------------------------
