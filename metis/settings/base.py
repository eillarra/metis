import os

from django.contrib.messages import constants as messages
from pathlib import Path
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parent.parent.parent

PACKAGE_ROOT = BASE_DIR / "metis"
SITE_ROOT = PACKAGE_ROOT / "site"


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
    "compressor",
    "django_vite",
    "inertia",
    "modeltranslation",
    # auth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # "allauth.socialaccount.providers.linkedin_oauth2",
    # api
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    # metis
    "metis",
    "metis.api",
    "metis.site",
    "metis.ugent_provider",
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
    "django.middleware.http.ConditionalGetMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "dnt.middleware.DoNotTrackMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "inertia.middleware.InertiaMiddleware",
]


ROOT_URLCONF = "metis.urls"
WSGI_APPLICATION = "metis.wsgi.application"


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

USE_I18N = True

LANGUAGE_CODE = "nl"
LANGUAGES = (
    ("en", "English"),
    ("nl", "Nederlands"),
)
LANGUAGE_COOKIE_NAME = "metis.language"
MODELTRANSLATION_LANGUAGES = ("en", "nl")
MODELTRANSLATION_TRANSLATION_FILES = ("metis.model_translations",)

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

AUTH_USER_MODEL = "metis.User"

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "dashboard"

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
    "linkedin_oauth2": {
        "SCOPE": ["r_emailaddress", "r_liteprofile"],
        "PROFILE_FIELDS": ["id", "firstName", "lastName", "emailAddress"],
    },
    "ugent": {
        "TENANT": os.environ.get("UGENT_TENANT_ID", "organizations"),
    },
}


# http://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_VERSION": "v1",
    "PAGE_SIZE": 50,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "COERCE_DECIMAL_TO_STRING": False,
}


# https://docs.djangoproject.com/en/dev/topics/templates/

INERTIA_LAYOUT = SITE_ROOT / "templates" / "vue" / "inertia.html"
DJANGO_VITE_ASSETS_PATH = BASE_DIR / "vue" / "dist"
DJANGO_VITE_STATIC_URL_PREFIX = "vite"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            SITE_ROOT / "templates",
            PACKAGE_ROOT / "admin" / "templates",
        ],
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
                "metis.context_processors.app",
                "metis.context_processors.sentry",
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
# https://docs.djangoproject.com/en/dev/ref/settings/#storages
# https://docs.djangoproject.com/en/dev/howto/static-files/
# https://docs.djangoproject.com/en/dev/howto/static-files/deployment/

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_URL = "/static/"
STATIC_ROOT = SITE_ROOT / "www" / "static"
STATICFILES_DIRS = [
    SITE_ROOT / "static",
    ("vite", DJANGO_VITE_ASSETS_PATH),
]
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "compressor.finders.CompressorFinder",
)

COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
COMPRESS_OFFLINE = True
COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)


# File uploads
# https://docs.djangoproject.com/en/dev/topics/http/file-uploads/

FILE_UPLOAD_PERMISSIONS = 0o644


# http://stackoverflow.com/questions/24071290/
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root

MEDIA_URL = "/media/"
MEDIA_ROOT = SITE_ROOT / "www" / "media"


# https://huey.readthedocs.io/en/latest/django.html

HUEY = {
    "name": "metis",
    "immediate": True,
}
