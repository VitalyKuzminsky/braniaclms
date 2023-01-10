"""
Django settings for braniaclms project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
# Вытаскиваем все переменные окружения:
from dotenv import load_dotenv

import django.contrib.messages.storage.session

import mainapp.context_processor

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')  # это работает для ручного развёртывания проекта


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2i+sh46c5f@2719%=nwpah#l_o76ti7pk0jj**(x)&iupzg^tg'

# SECURITY WARNING: don't run with debug turned on in production!
# отключаем DEBUG для prod
# DEBUG = True
DEBUG = True if os.getenv('DEBUG') == 'True' else False  # отработает даже, если нет значения или файла

ALLOWED_HOSTS = ["*"]

ENV_TYPE = os.getenv('ENV_TYPE', 'prod')

# if DEBUG:
#     INTERNAL_IPS = [
#         "127.0.0.1",
#     ]

# Настройки для подключения кеша
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Настройки для Отложеных задач через celery
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

# Внутренний встроенный миханизм Django по оперативному логированию:
# 500-ые ошибки с выстевленным флагом DEBUG = False, будут приходить на эту почту:
# ADMINS = (
#     ('email@email.ru', 'Oleg')
# )

# EMAIL_HOST = "localhost"
# EMAIL_PORT = "25"
# EMAIL_HOST_USER = "django@geekshop.local"
# EMAIL_HOST_PASSWORD = "geekshop"
# EMAIL_USE_SSL = True

# Настройка для работы на тесте
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "emails-tmp"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    # 'debug_toolbar',

    'authapp',
    'mainapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'braniaclms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],  # это папка для кастомизации админки
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mainapp.context_processor.my_context_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'braniaclms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if ENV_TYPE == 'local':
    DATABASES = {
        'default': {  # default - это псевдоним
            'ENGINE': 'django.db.backends.sqlite3',  # здесь могут быть и другие БД. sqlite3 создаётся по умолчанию
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'lms',
            'USER': 'postgres'
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

# Это интернационализация:
USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'  # эта настройка работает, когда проект в сети
if ENV_TYPE == 'local':
    STATICFILES_DIRS = [  # добавили в проект статику css, img, js, webfonts, favicon.ico, чтобы было видно локально
        BASE_DIR / 'static',
    ]
else:
    STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'authapp.User'
LOGIN_REDIRECT_URL = 'mainapp:index'
LOGOUT_REDIRECT_URL = 'mainapp:index'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

CRISPY_TEMPLATE_PACK = 'bootstrap4'  # мы испульзуем bootstrap версии 4 для раскрашивания форм

# # Логирование - файл-хендлер:
# LOG_FILE = BASE_DIR / "log" / "main_log.log"  # вручную создать папку log и добавить её в gitignore
#
# LOGGING = {
#     "version": 1,  # версия
#     "disable_existing_loggers": False,  # отключение других логеров флагом True
#     "formatters": {  # формат выводимой строки
#         "console": {  # логгер - консоль
#             "format": "[%(asctime)s] %(levelname)s %(name)s (%(lineno)d)% (message)s"  # текуще время, название уровня,
#             # название уровня, уровень строки (в которой всё вызывалось), сообщение
#         },
#     },
#     "handlers": {  # определение логеров
#         "file": {
#             "level": "INFO",
#             "class": "logging.FileHandler",
#             "filename": LOG_FILE,
#             "formatter": "console",
#         },
#         "console": {"class": "logging.StreamHandler", "formatter": "console"},  # класс, пакет логера, формат: консоль
#     },
#     "loggers": {  # настройки для логгеров
#         "django": {"level": "INFO", "handlers": ["file", "console"]},  # минимальный уровень сообщения INFO (собираются
#         # все логи от уровня INFO, включая его и выше), хендлер: консоль
#         # "mainapp": {
#         #     "level": "DEBUG",
#         #     "handlers": ["file"],
#         # },
#     },
# }

# Логирование - стрим-хендлер:
# LOGGING = {
#     "version": 1,  # версия
#     "disable_existing_loggers": False,  # отключение других логеров флагом True
#     "formatters": {  # формат выводимой строки
#         "console": {  # логгер - консоль
#             "format": "[%(asctime)s] %(levelname)s %(name)s (%(lineno)d)% (message)s"  # текуще время, название
#             # уровня, название уровня, уровень строки (в которой всё вызывалось), сообщение
#         },
#     },
#     "handlers": {  # определение логеров
#         # "file": {
#         #     "level": "DEBUG",
#         #     "class": "logging.FileHandler",
#         #     "filename": LOG_FILE,
#         #     "formatter": "console",
#         # },
#         "console": {"class": "logging.StreamHandler", "formatter": "console"},  # класс, пакет логера, формат: консоль
#     },
#     "loggers": {  # настройки для логгеров
#         "django": {"level": "INFO", "handlers": ["console"]},  # минимальный уровень сообщения INFO, хендлер: консоль
#         # "mainapp": {
#         #     "level": "DEBUG",
#         #     "handlers": ["file"],
#         # },
#     },
# }

LOG_FILE = BASE_DIR / "log" / "main_log.log"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "[%(asctime)s] %(levelname)s %(name)s (%(lineno)d) %(message)s"
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
            "formatter": "console",
        },
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
    },
    "loggers": {
        "django": {"level": "INFO", "handlers": ["file", "console"]},
    },
}

# Для перевода собираем локаль - информация по языку
LOCALE_PATHS = [BASE_DIR / 'locale']
