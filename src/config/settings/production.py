import os

from .base import MIDDLEWARE


# ----------------------------------------------------------------


# --DATABASES-----------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
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
        "host": os.getenv("REDIS_HOST", "redis"),
        "port": int(os.getenv("REDIS_PORT", 6379)),
        "db": int(os.getenv("REDIS_Q_DB", 2)),
    },
}
# ----------------------------------------------------------------


# ---Production whitenoise----------------------------------------
if int(os.getenv("ENABLE_WHITENOISE", default=0)):
    MIDDLEWARE += [
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]
    STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"

ENABLE_MEDIA_SERVE_IN_LOCAL = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
# ----------------------------------------------------------------
