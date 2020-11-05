"""Параметры приложения для разработки."""
import os

from .base import *  # noqa: F403

DEBUG = os.getenv('DEBUG', 'True') == 'True'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# INSTALLED_APPS.append('silk')
MIDDLEWARE.extend([  # noqa: F405
    # 'silk.middleware.SilkyMiddleware',
    'request_logging.middleware.LoggingMiddleware'
])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        # 'sql_console': {
        #     'level': 'DEBUG',
        #     'class': 'logging.StreamHandler',
        # }
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',  # change debug level as appropiate
            'propagate': False,
        },
        # 'django.db.backends': {
        #     'handlers': ['sql_console'],
        #     'level': 'DEBUG'
        # }
    },
}

EMPLOYEE_TEST_NUMBER = os.getenv(
    'EMPLOYEE_TEST_NUMBER', '89241096563',  # номер Никиты В.
)
CLIENT_TEST_NUMBER = os.getenv(
    'CLIENT_TEST_NUMBER', '89244514835',  # номер Павла Б.
)
