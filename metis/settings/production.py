import os
import re
import sentry_sdk

from django.core.exceptions import DisallowedHost
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .base import *  # noqa


DEBUG = False

ALLOWED_HOSTS = (os.environ.get("DJANGO_ALLOWED_HOST", "metis.ugent.be"),)
MEDIA_ROOT = "/storage/media/"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True


# sendfile

SENDFILE_ROOT = f"{MEDIA_ROOT}private"
SENDFILE_URL = "/-internal"


# https://docs.sentry.io/platforms/python/guides/django/


def set_user_id(event, hint):
    if "request" in event and event["request"].user.is_authenticated:
        event["user"] = {"id": event["request"].user.id}
    return event


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DJANGO_DSN", None),
    release=os.environ.get("GIT_REV", None),
    environment=os.environ.get("DJANGO_ENV", "production"),
    integrations=[DjangoIntegration(), RedisIntegration()],
    ignore_errors=[DisallowedHost],
    traces_sample_rate=0.1,
    _experiments={
        "profiles_sample_rate": 0.1,
    },
    # pii
    send_default_pii=False,
    before_send=set_user_id,
)


# https://docs.djangoproject.com/en/dev/topics/cache/

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
    },
    "staticfiles": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "django-staticfiles",
    },
}

CACHE_MIDDLEWARE_SECONDS = 30
USE_ETAGS = True


# https://docs.djangoproject.com/en/dev/topics/email/

DEFAULT_FROM_EMAIL = "METIS <metis@ugent.be>"
SERVER_EMAIL = "metis@ugent.be"
EMAIL_SUBJECT_PREFIX = "[METIS] "

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
    "name": "metis",
    "connection": {
        "url": f"{os.environ.get('REDIS_URL', 'redis://localhost:6379')}/10",
    },
}


# https://github.com/MrBin99/django-vite

DJANGO_VITE_DEV_MODE = False


def immutable_file_test(path, url):
    # Vite generates files with 8 hash digits
    # Match filename with 8 or 12 hex digits before the extension
    # e.g. app.db8f2edc0c8a.js
    return re.match(r"^.+\.[0-9a-f]{8,12}\..+$", url)


WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test
