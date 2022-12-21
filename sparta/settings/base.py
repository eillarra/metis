import os

from django.contrib.messages import constants as messages
from urllib.parse import urlparse


PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PROJECT_ROOT = os.path.abspath(os.path.join(PACKAGE_ROOT, os.pardir))
SITE_ROOT = os.path.join(PACKAGE_ROOT, "site")


# General configuration

DEBUG = True

ADMINS = (("eillarra", "eneko.illarramendi@ugent.be"),)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "DJANGO_SECRET_KEY")
SITE_ID = int(os.environ.get("SITE_ID", 1))

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.messages",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # helpers
    "captcha",
    "compressor",
    # auth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # "allauth.socialaccount.providers.google",
    # "allauth.socialaccount.providers.linkedin_oauth2",
    "allauth.socialaccount.providers.microsoft",  # ugent
    # api
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    # sparta
    "sparta",
    "sparta.api",
    "sparta.site",
    # tasks
    "huey.contrib.djhuey",
    # admin
    "django.contrib.admin",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "dnt.middleware.DoNotTrackMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
]


ROOT_URLCONF = "sparta.urls"
WSGI_APPLICATION = "sparta.wsgi.application"


# https://docs.djangoproject.com/en/dev/ref/settings/#databases

db = urlparse(os.environ.get("DATABASE_URL"))
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": db.path[1:],
        "USER": db.username,
        "PASSWORD": db.password,
        "HOST": db.hostname,
        "PORT": db.port,
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Time zones
# https://docs.djangoproject.com/en/dev/topics/i18n/timezones/

USE_TZ = True
TIME_ZONE = "Europe/Brussels"


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "nl"
USE_I18N = False

FIRST_DAY_OF_WEEK = 1


# Security
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

# CSRF / Cookie

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
CSRF_USE_SESSIONS = not DEBUG

# XFRAME

X_FRAME_OPTIONS = "DENY"

# CORS

CORS_ORIGIN_ALLOW_ALL = True

# Account

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptPasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]

ACCOUNT_ACTIVATION_DAYS = 7
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"

# Social accounts

SOCIALACCOUNT_PROVIDERS = {
    "google": {"SCOPE": ["profile", "email"], "AUTH_PARAMS": {"access_type": "online"}},
    "linkedin_oauth2": {
        "SCOPE": ["r_emailaddress", "r_liteprofile"],
        "PROFILE_FIELDS": ["id", "firstName", "lastName", "emailAddress"],
    },
    "microsoft": {"TENANT": "organizations"},
}


# http://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_VERSION": "v1",
    "PAGE_SIZE": 50,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "COERCE_DECIMAL_TO_STRING": False,
}


# https://docs.djangoproject.com/en/dev/topics/templates/

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(SITE_ROOT, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

COUNTRIES_OVERRIDE = {
    "GB": "United Kingdom",
    "US": "United States",
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
# https://docs.djangoproject.com/en/dev/howto/static-files/deployment/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, "www", "static")
STATICFILES_DIRS = (os.path.join(SITE_ROOT, "static"),)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "compressor.finders.CompressorFinder",
)
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
COMPRESS_OFFLINE = True
COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)


# File uploads
# https://docs.djangoproject.com/en/dev/topics/http/file-uploads/

FILE_UPLOAD_PERMISSIONS = 0o644


# http://stackoverflow.com/questions/24071290/
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, "www", "media")


# https://huey.readthedocs.io/en/latest/django.html

HUEY = {
    "name": "sparta",
    "immediate": True,
}


# reCAPTCHA
# https://github.com/praekelt/django-recaptcha#installation

RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY", "RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY", "RECAPTCHA_PRIVATE_KEY")
RECAPTCHA_USE_SSL = True
NOCAPTCHA = True  # For using reCAPTCHA v2
