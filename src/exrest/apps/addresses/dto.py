"""Модуль со списком DTO для работы с адресами."""

from schematics import types

from exrest.apps.addresses.enums import AddressTypeEnum, GeoPointsAccuracy
from exrest.common.dto import DTO


class AddressDTO(DTO):
    """DTO адреса."""

    id = types.IntType()  # noqa: A003
    city = types.StringType(required=True)
    street = types.StringType(required=True)
    house = types.StringType(required=True)
    building = types.StringType()
    apartment = types.StringType()
    floor = types.StringType()
    entrance = types.StringType()
    comment = types.StringType()
    lat = types.FloatType()
    lon = types.FloatType()
    fias_id = types.UUIDType()


class SuggestionAddressParamsDTO(DTO):
    """DTO поиска адреса в геосервисе."""

    from_bound = types.StringType(
        choices=AddressTypeEnum.choices(), required=True)
    to_bound = types.StringType(
        choices=AddressTypeEnum.choices(), required=True)
    query = types.StringType(required=True)
    region_fias_id = types.UUIDType()
    area_fias_id = types.UUIDType()
    city_fias_id = types.UUIDType()
    settlement_fias_id = types.UUIDType()
    street_fias_id = types.UUIDType()
    count = types.IntType(default=5)

    class Options:
        serialize_when_none = False


class SuggestionAddressDTO(DTO):
    """DTO подсказки адреса."""

    value = types.StringType()
    fias_id = types.UUIDType()
    lat = types.StringType()
    lon = types.StringType()
    fias_level = types.StringType(
        choices=AddressTypeEnum.choices(),
    )


class SuggestionsDTO(DTO):
    """DTO списка подсказок."""

    type = types.StringType(choices=AddressTypeEnum.choices(), required=True)  # noqa: A003, E501
    suggestions = types.ListType(types.ModelType(SuggestionAddressDTO))


class GeoserviceSuggestionDataDTO(DTO):
    """DTO данных подсказки из геосервиса."""

    fias_id = types.UUIDType()
    geo_lat = types.FloatType()
    geo_lon = types.FloatType()
    qc_geo = types.IntType(choices=GeoPointsAccuracy.choices())
    fias_level = types.IntType()


class GeoserviceSuggestionDTO(DTO):
    """DTO подсказки (с метаданными) из геосервиса."""

    data = types.ModelType(GeoserviceSuggestionDataDTO)
    unrestricted_value = types.StringType()
    value = types.StringType()


class GeoserviceSuggestionResponseDTO(DTO):
    """DTO списка подсказок из геосервиса."""

    suggestions = types.ListType(types.ModelType(GeoserviceSuggestionDTO))
