from .base import *  # noqa


DEBUG = True
TEST = True

ALLOWED_HOSTS = ("localhost",)
INTERNAL_IPS = ("127.0.0.1",)


# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "dev.db",
    },
}


# https://docs.djangoproject.com/en/dev/topics/cache/

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
}


# https://docs.djangoproject.com/en/dev/topics/email/

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# https://django-compressor.readthedocs.io/en/stable/settings/

COMPRESS_ENABLED = False
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
