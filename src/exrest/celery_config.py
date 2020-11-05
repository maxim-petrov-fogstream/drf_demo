"""Конфигурация для celery."""
from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings
from celery import Celery

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exrest.settings.dev')

app = Celery('exrest')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)

SENTRY_DSN = os.getenv('SENTRY_DSN')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=(CeleryIntegration(),)
    )


@app.task(bind=True)
def debug_task(self):
    """Тестовая таска для дебага."""
    print('Request: {0!r}'.format(self.request))
