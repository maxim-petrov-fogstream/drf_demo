from rest_framework.routers import DefaultRouter

from exrest.apps.addresses import views

router = DefaultRouter()
router.register('addresses', views.AddressViewSet, basename='addresses')
