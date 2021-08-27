"""
Django config for doc_manager project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/config/

For the full list of config and their values, see
https://docs.djangoproject.com/en/2.1/ref/config/
"""
import os

APPEND_SLASH = False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


LANGUAGES = (
    ("zh-cn", u"简体中文"),  # instead of 'zh-CN'
    ("zh-tw", u"繁體中文"),  # instead of 'zh-TW'
)

# Quick-start development config - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.auth",
    "vending_machine.apps.VendingMachineConfig",
    "rest_framework",
    "rest_framework.authtoken",
    "django_extensions",
    "corsheaders",
    "guardian",
    "django.contrib.postgres",
]


REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "vending_machine.views.exceptions.custom_exception_handler",
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
]

CORS_ORIGIN_WHITELIST = (
    "localhost:3000",
    "localhost:3001",
)

project_root = os.path.normpath(os.path.join(__file__, "../../"))

DB_SEARCH_ENABLED = False

DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # i.e. 50 MB

ROOT_URLCONF = "vending_machine.urls"
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # this is default
)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "vending_machine.wsgi.application"
TOKEN_EXPIRED_AFTER_SECONDS = 86400

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

db_name = os.getenv("POSTGRES_DB", "vending_machine_development")
db_user = os.getenv("POSTGRES_USER", "")
db_password = os.getenv("POSTGRES_PASSWORD", "")
host = os.getenv("POSTGRES_HOST", "localhost")
port = os.getenv("POSTGRES_PORT", "5432")

DATABASES = {
    "default": {
        "ENGINE": "django_multitenant.backends.postgresql",
        "NAME": db_name,
        "USER": db_user,
        "PASSWORD": db_password,
        "HOST": host,
        "PORT": port,
    },
    "test": {
        "ENGINE": "django_multitenant.backends.postgresql",
        "NAME": f'{db_name}_test',
        "USER": db_user,
        "PASSWORD": db_password,
        "HOST": host,
        "PORT": port,
    },
    # "production": {
    #     "ENGINE": "django_multitenant.backends.postgresql",
    #     "NAME": "doc_manager_production",
    #     "USER": "proxyuser",
    #     "PASSWORD": "a2k35jaw9fka",
    #     "HOST": "35.200.230.79",
    #     "PORT": "5432",
    # },
}

TIME_ZONE = "Asia/Kolkata"
USE_TZ = True
AUTH_USER_MODEL = "vending_machine.User"
STATIC_URL = "/static/"
