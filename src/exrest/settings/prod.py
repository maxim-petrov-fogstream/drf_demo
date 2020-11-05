"""Параметры приложения для запуска в production."""
from .base import *  # noqa: F401, F403


DEBUG = False

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
