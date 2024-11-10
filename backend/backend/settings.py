import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite3")

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(" ")

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

YANDEX_API_WEATHER_KEY = os.getenv("YANDEX_API_WEATHER_KEY")
YANDEX_WEATHER_URL = os.getenv("YANDEX_WEATHER_URL",)

# CELERY_BROKER_URL = 'redis://redis:6379/0'
# CELERY_RESULT_BACKEND = 'redis://redis-server:6379/0'

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_filters",
    "weather.apps.WeatherConfig",
    "corsheaders",

]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "querycount.middleware.QueryCountMiddleware",
]
ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Подключение к БД sqlite3 или postgresql

if DB_ENGINE == "sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

if DB_ENGINE == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", default="django"),
            "USER": os.getenv("POSTGRES_USER", default="django_user"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="django"),
            "HOST": os.getenv("DB_HOST", default="doct24_db"),
            "PORT": os.getenv("DB_PORT", default=5432),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Настройка Статики и Медиа backenda

STATIC_URL = "/backend_static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/backend_media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Настройка REST_FRAMEWORK

REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%d.%m.%Y %H:%M:%S",

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

    "DATE_INPUT_FORMATS": ["%d.%m.%Y"],
    # "DEFAULT_PAGINATION_CLASS":
    #     "rest_framework.pagination.LimitOffsetPagination",
    # "PAGE_SIZE": int(os.getenv("PAGE_SIZE", 10)),
}


# Настройка SPECTACULAR_SETTINGS для SWAGGERA

SPECTACULAR_SETTINGS = {
    "TITLE": "Weather_data",
    "VERSION": "1.0.0",
    "DESCRIPTION": "Weather_data: Backend",
    "CONTACT": {
        "name": "Weather_data",
        "url": "https://github.com/DPavlen/Weather_data",
        "email": "jobpavlenko@yandex.ru",
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_COERCE_PATH_PK_SUFFIX": True,
    "SORT_OPERATIONS": True,
    "SCHEMA_PATH_PREFIX": r"/api/",
}

# Настройки Celery
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# Настройки Django-cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/1",
    }
}