import os

from .base import *  # noqa


DEBUG = False

ALLOWED_HOSTS = (os.environ.get("DJANGO_ALLOWED_HOST", "sparta.ugent.be"),)
MEDIA_ROOT = "/storage/media/"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True


# sendfile

SENDFILE_ROOT = f"{MEDIA_ROOT}private"
SENDFILE_URL = "/-internal"


# https://docs.djangoproject.com/en/dev/topics/cache/

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
    },
    "staticfiles": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": "django-staticfiles"},
}

CACHE_MIDDLEWARE_SECONDS = 30
USE_ETAGS = True


# https://docs.djangoproject.com/en/dev/topics/email/

DEFAULT_FROM_EMAIL = "SPARTA <sparta@ugent.be>"
SERVER_EMAIL = "sparta@ugent.be"
EMAIL_SUBJECT_PREFIX = "[SPARTA] "

EMAIL_HOST = "smtprelay.ugent.be"
EMAIL_PORT = 25


# https://docs.djangoproject.com/en/dev/topics/logging/#django-security
# https://docs.sentry.io/platforms/python/?platform=python

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
}


# https://huey.readthedocs.io/en/latest/django.html

HUEY = {
    "huey_class": "huey.RedisHuey",
    "immediate": False,
    "name": "sparta",
    "connection": {
        "url": f"{os.environ.get('REDIS_URL', 'redis://localhost:6379')}/10",
    },
}
