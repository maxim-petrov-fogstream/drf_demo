"""Модуль с моделями адреса."""

from django.db import models

from exrest.common.exceptions import ValidatingError
from exrest.common.models import LocationMixin, BaseModel, ValidatingMixin


class Address(ValidatingMixin, LocationMixin, BaseModel):
    """Таблица адресов."""

    city = models.CharField('город', max_length=256, null=True)
    street = models.CharField('улица', max_length=256, null=True)
    house = models.CharField('дом', max_length=256, null=True)
    building = models.CharField(
        'строение',
        max_length=256,
        null=True,
        blank=True
    )
    apartment = models.CharField(
        'квартира',
        max_length=256,
        null=True,
        blank=True
    )
    floor = models.IntegerField('этаж', null=True, blank=True)
    entrance = models.CharField(
        'подъезд',
        max_length=256,
        null=True,
        blank=True
    )
    comment = models.TextField('комментарий', null=True, blank=True)
    additional_info = models.TextField('комментарий', null=True, blank=True)
    fias_id = models.UUIDField(
        verbose_name='Идентификатор в ФИАС',
        null=True,
        blank=True
    )
    is_main = models.BooleanField('основной', default=False)
    stop_date = models.DateField(
        'дата удаления', null=True, blank=True, default=None
    )
    invalid_coordinates = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.city or ""} {self.street or ""} {self.house or ""}'

    class Meta:
        verbose_name = 'адрес'
        verbose_name_plural = 'адреса'

    @classmethod
    def validate_some(cls, instance: models.Model = None, fields: dict = None,
                      raise_exception=False):
        fields_dict = fields or {}
        obj = instance or cls(**fields_dict)

        errors = {}

        if not obj.lat:
            errors['lat'] = 'Обязательное поле.'
        if not obj.lon:
            errors['lon'] = 'Обязательное поле.'
        if obj.invalid_coordinates:
            errors['invalid_coordinates'] = 'Некорректные координааты.'

        if errors and raise_exception:
            raise ValidatingError(errors)

        return not errors
