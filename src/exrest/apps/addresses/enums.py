from exrest.common.enums import IntegerChoicesEnum, StringChoicesEnum


class AddressTypeEnum(StringChoicesEnum):
    """Типы объектов."""

    HOUSE = 'house', 'дом'
    STREET = 'street', 'улица'
    SETTLEMENT = 'settlement', 'населённый пункт'
    CITY = 'city', 'город'
    AREA = 'area', 'район'
    REGION = 'region', 'регион'


FIAS_LEVEL_MAPPING = {
    1: AddressTypeEnum.REGION.value,
    2: AddressTypeEnum.REGION.value,
    3: AddressTypeEnum.AREA.value,
    4: AddressTypeEnum.CITY.value,
    5: AddressTypeEnum.SETTLEMENT.value,
    6: AddressTypeEnum.SETTLEMENT.value,
    65: AddressTypeEnum.SETTLEMENT.value,
    7: AddressTypeEnum.STREET.value,
    8: AddressTypeEnum.HOUSE.value
}


class GeoPointsAccuracy(IntegerChoicesEnum):
    """Точность координат."""

    PRECISE = 0, 'точные координаты'
    NEAREST = 1, 'ближайший дом'
    STREET = 2, 'улица',
    SETTLEMENT = 3, 'населённый пункт'
    CITY = 4, 'город'
    UNKNOWN = 5, 'координаты не определены'
