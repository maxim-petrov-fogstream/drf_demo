"""Модуль с сериализаторами адресов."""

from rest_framework import serializers

from exrest.apps.addresses.models import Address
from exrest.apps.addresses.enums import AddressTypeEnum


class AddressSerializer(serializers.ModelSerializer):
    """Сериализатор адреса."""

    class Meta:
        model = Address
        exclude = ('created_date', 'modified_date')


class SuggestionsRequestSerializer(serializers.Serializer):
    """Сериализатор запроса на получение подсказок адреса."""

    type = serializers.ChoiceField(choices=AddressTypeEnum.values())  # noqa: A003, E501
    query = serializers.CharField()
    regions_fias_id = serializers.UUIDField(required=False)
    area_fias_id = serializers.UUIDField(required=False)
    city_fias_id = serializers.UUIDField(required=False)
    settlement_fias_id = serializers.UUIDField(required=False)
    street_fias_id = serializers.UUIDField(required=False)
    count = serializers.IntegerField(required=False, default=5)


class SuggestionSerializer(serializers.Serializer):
    """Сериализатор подсказки адреса."""

    value = serializers.CharField()
    fias_id = serializers.UUIDField()
    lat = serializers.CharField()
    lon = serializers.CharField()


class SuggestionsResponseSerializer(serializers.Serializer):
    """Сериализатор ответа на запрос подсказок адреса."""

    type = serializers.ChoiceField(choices=AddressTypeEnum.values())  # noqa: A003, E501
    suggestions = SuggestionSerializer(many=True)


class ReverseGeocodingRequestSerializer(serializers.Serializer):
    """Сериализатор запроса на обратный геокодинг."""

    query = serializers.CharField()


class ReverseGeocodingResponseSerializer(serializers.Serializer):
    """Сериализатор ответа на обратный геокодинг."""

    address = serializers.CharField()
    lat = serializers.CharField()
    lon = serializers.CharField()
