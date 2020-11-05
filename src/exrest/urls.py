"""Конфигурация URL для exrest."""
from django.conf import settings
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from exrest.apps.addresses.urls import router as addresses_router
from exrest.apps.auth.urls import router as auth_router
from exrest.apps.calls.urls import router as calls_api_router
from exrest.apps.clients.urls import (
    router as clients_router,
    nester_clients_router,
    nester_orders_history_router
)
from exrest.apps.comments.urls import router as comments_router
from exrest.apps.crews.urls import router as crews_router, nester_crews_router
from exrest.apps.employees.urls import router as employees_router
from exrest.apps.enums.urls import router as enums_api_router
from exrest.apps.fcm.urls import router as fcm_router
from exrest.apps.landing.urls import router as landing_router
from exrest.apps.orders.urls import router as orders_router
from exrest.apps.payments.urls import router as acquiring_router
from exrest.apps.schedule.urls import router as schedule_router
from exrest.apps.shifts.urls import (
    router as shifts_router,
    nester_shifts_router
)
from exrest.apps.sms_api.urls import router as sms_api_router
from exrest.apps.stats.urls import router as stats_router
from exrest.apps.stocks.urls import router as stocks_router
from exrest.apps.users.urls import router as users_router
from exrest.apps.vrp.urls import router as vrp_router
from exrest.common.admin import admin_site
from exrest.common.router import ExtendableRouter

router = ExtendableRouter()
router.extend(auth_router)
router.extend(crews_router)
router.extend(nester_crews_router)
router.extend(employees_router)
router.extend(shifts_router)
router.extend(nester_shifts_router)
router.extend(clients_router)
router.extend(nester_clients_router)
router.extend(nester_orders_history_router)
router.extend(users_router)
router.extend(landing_router)
router.extend(comments_router)
router.extend(addresses_router)
router.extend(stats_router)
router.extend(sms_api_router)
router.extend(enums_api_router)
router.extend(stocks_router)
router.extend(calls_api_router)
router.extend(fcm_router)
router.extend(orders_router)
router.extend(schedule_router)
router.extend(vrp_router)
router.extend(acquiring_router)

urlpatterns = [
    path('admin/', admin_site.urls),
    path('api/v2/', include(router.urls))
]

if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title='Expedition REST API',
            default_version='v2',
            description='REST API для внутренних сервисов и клиентов',
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        path(r'^swagger(?P<format>\.json|\.yaml)$',
             schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger',
             schema_view.with_ui('swagger', cache_timeout=0),
             name='schema-swagger-ui'),
        path('redoc',
             schema_view.with_ui('redoc', cache_timeout=0),
             name='schema-redoc'),
        # path('silk/', include('silk.urls', namespace='silk'))
    ]
