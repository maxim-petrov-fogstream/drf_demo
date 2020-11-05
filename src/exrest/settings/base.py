"""Базовые параметры приложения.

Больше информации об этом файле
https://docs.djangoproject.com/en/2.1/topics/settings/

Для получения полного списка параметров, см.
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import logging
import os
import sys

from django.conf.global_settings import *  # noqa: F401, F403
# from django.contrib import admin
# Корень исход
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

# =============================================================================
# Основные пути приложения


SOURCES_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')
)

# Корень приложения
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../api')
)

# Пути для медиа
MEDIA_ROOT = os.path.join(SOURCES_ROOT, 'media')
MEDIA_URL = '/media/'

# Пути для статики
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(SOURCES_ROOT, 'static')

# Пути до статики в пакетах
STATICFILES_DIRS = []

sys.path.insert(0, os.path.join(BASE_DIR))

# =============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'sosecret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(', ')

# =============================================================================

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'channels',
    'mptt',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'rolepermissions',
    'corsheaders',
    'solo',
    'django_filters',
    'phonenumber_field',
    'fcm_django',
]

LOCAL_APPS = [
    'exrest.common',
    'exrest.apps.addresses',
    'exrest.apps.background_tasks',
    'exrest.apps.clients',
    'exrest.apps.crews',
    'exrest.apps.shifts',
    'exrest.apps.stocks',
    'exrest.apps.merman',
    'exrest.apps.employees',
    'exrest.apps.orders',
    'exrest.apps.vrp',
    'exrest.apps.comments',
    'exrest.apps.landing',
    'exrest.apps.custom_settings',
    'exrest.apps.sms_api',
    'exrest.apps.users',
    'exrest.apps.enums',
    'exrest.apps.calls',
    'exrest.apps.fcm',
    'exrest.apps.schedule',
    'exrest.apps.payments'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'exrest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '../templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

# =============================================================================
# Параметры сервера электронной почты

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', False)

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# =============================================================================
# Параметры подключения к БД

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB', 'exrest'),
        'USER': os.getenv('POSTGRES_USER', 'exrest'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'exrest'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5436'),
    }
}

ATOMIC_REQUESTS = True

# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Vladivostok'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Celery
CELERY_BROKER_URL = os.getenv(
    'CELERY_BROKER_URL', 'redis://localhost:6379/1')
CELERY_RESULT_BACKEND = os.getenv(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = os.getenv(
    'CELERY_TASK_SERIALIZER', 'json')
CELERY_RESULT_SERIALIZER = os.getenv(
    'CELERY_RESULT_SERIALIZER', 'json')
CELERY_TIMEZONE = os.getenv(
    'CELERY_TIMEZONE', 'Asia/Vladivostok')
CELERY_BEAT_SCHEDULE = {}

ASGI_APPLICATION = 'exrest.routing.application'

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_SCAN_COUNT = os.getenv('REDIS_SCAN_COUNT', 1000)

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_HOST, REDIS_PORT)]
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': (
            f'redis://{REDIS_HOST}:'
            f'{REDIS_PORT}/'
            f'{os.getenv("CACHE_REDIS_DB", "2")}'
        ),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'local': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}

REDIS_COORDS_DB = int(os.getenv('REDIS_COORDS_DB', '5'))

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # <-- And here
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'PAGE_SIZE': 10
}

ROLEPERMISSIONS_MODULE = 'exrest.common.roles'

MERMAN_API_URL = os.getenv(
    'MERMAN_API_URL',
    'http://merman-wrapper.expedition.176.58.96.107.xip.io/'
)

GEOSERVICE_API_URL = os.getenv(
    'GEOSERVICE_API_URL',
    'http://geoservice.expedition.81.29.132.166.nip.io/'
)

VRP_RESOLVER_API_URL = os.getenv(
    'VRP_RESOLVER_API_URL',
    'http://vrp-resolver.expedition.176.58.96.107.xip.io'
)

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

CORS_ORIGIN_ALLOW_ALL = os.getenv('CORS_ALLOW_ALL', 'False') == 'True'

MERMAN_LOAD_PAGE_SIZE = os.getenv('MERMAN_LOAD_PAGE_SIZE', 1000)

RABBIT_CONNECTION_URL = os.getenv(
    'RABBIT_CONNECTION_URL', 'amqp://guest:guest@localhost:5672//')

# =============================================================================
# SENTRY

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)

SENTRY_DSN = os.getenv('SENTRY_DSN')
if SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            sentry_logging
        ]
    )

SHIFTS_LOGS_DIRECTORY_PATH = os.getenv(
    'SHIFTS_LOGS_DIRECTORY_PATH', '/application/logs'
)

REDIS_CREW_KEY_EXPIRED_TIME = int(
    os.getenv('REDIS_CREW_KEY_EXPIRED_TIME', 300)
)
REDIS_CURRENT_SHIFT_KEY_EXPIRED_TIME = int(os.getenv(
    'REDIS_CURRENT_SHIFT_KEY_EXPIRED_TIME', 900
))

SHIFT_EXTRA_RANGE_TIME_HOURS = int(
    os.getenv('SHIFT_EXTRA_RANGE_TIME_HOURS', 1)
)

# Тестовые номера, если настройка задана
# звонок всегда будет происходить на них

EMPLOYEE_TEST_NUMBER = os.getenv(
    'EMPLOYEE_TEST_NUMBER', None  # FIXME: Убрать ближе к релизу
)
CLIENT_TEST_NUMBER = os.getenv(
    'CLIENT_TEST_NUMBER', None  # FIXME: Убрать ближе к релизу
)

CLIENTS_GROUPS_SYNC_PERIOD_TIME = int(
    os.getenv('CLIENTS_GROUPS_SYNC_PERIOD_TIME', 30)
)
CARS_SYNC_PERIOD_TIME = int(os.getenv('CARS_SYNC_PERIOD_TIME', 300))
CLIENTS_AND_ORDER_SYNC_PERIOD_TIME = int(
    os.getenv('CLIENTS_AND_ORDER_SYNC_PERIOD_TIME', 45)
)
PRODUCT_SYNC_PERIOD_TIME = int(os.getenv('PRODUCT_SYNC_PERIOD_TIME', 300))
EMPLOYEE_SYNC_PERIOD_TIME = int(os.getenv('EMPLOYEE_SYNC_PERIOD_TIME', 300))

BACKGROUND_TASKS_DAYS_LIVE = int(os.getenv('BACKGROUND_TASKS_DAYS_LIVE', 3))
BACKGROUND_TASKS_DEFAULT_PERIOD = int(
    os.getenv('BACKGROUND_TASKS_DEFAULT_PERIOD', 60)
)
CLEAN_TASKS_PERIOD_TIME = int(
    os.getenv('CLEAN_TASK_PERIOD_TIME', 60 * 60 * 24)
)

ADMIN_SITE_HEADER = 'АИС Экспедитор'

# Данные для API Билайн по отправке сообщений
BEELINE_API_URL = 'http://www.beeline.amega-inform.ru'
BEELINE_API_USER = os.getenv('BEELINE_API_USER')
BEELINE_API_PASSWORD = os.getenv('BEELINE_API_PASSWORD')
BEELINE_API_SENDER = os.getenv('BEELINE_API_SENDER', 'Voda-Les.ru')

# Настройки одноразового кода авторизации
OTC_LENGTH = int(os.getenv('OTC_LENGTH', 4))
OTC_DELAY = int(os.getenv('OTC_DELAY', 600))

# Настройки сервиса отправки Push-уведомлений
FCM_DJANGO_SETTINGS = {
    'FCM_SERVER_KEY': os.getenv('FCM_API_KEY'),
}

FAKE_COORDS_REQUEST = os.getenv('FAKE_COORDS_REQUEST', True)

SHIFT_TIMEDELTA = int(os.getenv('SHIFT_TIMEDELTA', 60))

SBERBANK_API_USERNAME = os.getenv('SBERBANK_API_USERNAME')
SBERBANK_API_PASSWORD = os.getenv('SBERBANK_API_PASSWORD')
SBERBANK_GATEWAY_URL = os.getenv(
    'SBERBANK_GATEWAY_URL',
    'https://3dsec.sberbank.ru/payment/rest/'
)
ANDROID_LINK_TO_APP = os.getenv('ANDROID_LINK_TO_APP')
IOS_LINK_TO_APP = os.getenv('IOS_LINK_TO_APP')
PAYMENTS_STATUSES_SYNC_PERIOD_TIME = int(
    os.getenv('PAYMENTS_STATUSES_SYNC_PERIOD_TIME', 60)
)

ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': f'redis://{REDIS_HOST}:{REDIS_PORT}/'
               f'{os.getenv("CACHE_REDIS_DB", "2")}',
        'default_timeout': 60 * 60
    }
}

FAKE_VRP_CREW_RECALCULATE = (
    os.getenv('FAKE_VRP_CREW_RECALCULATE', 'False') == 'True'
)

MERMAN_SHIFT_ONLINE_SYNC = (
    os.getenv('MERMAN_SHIFT_ONLINE_SYNC', 'False') == 'True'
)


MERMAN_DEFAULT_PAGE_SIZE = int(os.getenv('MERMAN_DEFAULT_PAGE_SIZE', 500))

RECALCULATE_ROUTE_AFTER_COMPLETE = (
    os.getenv('RECALCULATE_ROUTE_AFTER_COMPLETE', 'False') == 'True'
)
