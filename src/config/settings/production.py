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

SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "1") == "1"

SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "1") == "1"

CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "1") == "1"

SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "3600"))
SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)
# ----------------------------------------------------------------
