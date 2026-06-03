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
