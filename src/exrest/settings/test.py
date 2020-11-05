"""Параметры приложения для запуска в test."""
from .base import *  # noqa: F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'exrest_test',
        'USER': 'exrest',
        'PASSWORD': 'exrest',
        'HOST': 'postgres',  # Если недоступен, то попробует localhost
    }
}

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')  # noqa: F405
REDIS_PORT = os.getenv('REDIS_PORT', '6379')  # noqa: F405

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

SHIFTS_LOGS_DIRECTORY_PATH = '/tmp/shifts'
