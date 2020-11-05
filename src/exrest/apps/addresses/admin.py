"""Модуль с настройками модели адреса в админке."""

from django.contrib import admin

from exrest.apps.addresses.models import Address
from exrest.common.admin import admin_site


@admin.register(Address, site=admin_site)
class AddressAdmin(admin.ModelAdmin):
    """Настройки модели адреса в админке."""

    list_display = (
        'lat', 'lon', 'city', 'street', 'house',
        'building', 'entrance', 'floor', 'apartment', 'comment'
    )
    list_display_links = ('city', 'street', 'house',)
    search_fields = ('city', 'street', 'house')
