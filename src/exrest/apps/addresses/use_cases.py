"""Модуль со сценариями по работе с адресами."""

from exrest.apps.addresses.dto import (
    SuggestionAddressParamsDTO, GeoserviceSuggestionResponseDTO,
    SuggestionsDTO, SuggestionAddressDTO, GeoserviceSuggestionDTO,
    GeoserviceSuggestionDataDTO)
from exrest.apps.addresses.enums import GeoPointsAccuracy, FIAS_LEVEL_MAPPING
from exrest.apps.geo.gateways import GeoserviceGateway
from exrest.common.use_cases import BaseUseCase


class GetAddressesSuggestionsUseCase(BaseUseCase):
    """Сценарий на получение подсказок по указанному адресу."""

    @classmethod
    def execute(cls,
                suggestions_address_params_dto: SuggestionAddressParamsDTO
                ) -> SuggestionsDTO:
        """Метод запускает сценарий.

        Сценарий:
            1. Получить подсказки из геосервиса
            2. Привести к виду для ответа клиенту

        :param suggestions_address_params_dto: параметры запроса подсказок
        :return: DTO списка подсказок
        """
        raw_suggestions = GeoserviceGateway().get_suggestions(
            suggestions_address_params_dto.to_native()
        )
        raw_suggestions.update({
            'type': suggestions_address_params_dto.from_bound
        })
        suggestions = SuggestionsDTO(raw_suggestions)

        suggestions.suggestions = [
            cls._create_suggestion_address_dto(geoservice_suggestion)
            for geoservice_suggestion in (
                GeoserviceSuggestionResponseDTO(raw_suggestions).suggestions
            )
        ]

        return suggestions

    @staticmethod
    def _create_suggestion_address_dto(
            geoservice_dto: GeoserviceSuggestionDTO
    ) -> SuggestionAddressDTO:
        """Метод создает DTO подсказок из подсказок геосервиса.

        :param geoservice_dto: DTO подсказки из геосервиса

        :return: DTO подсказки для ответа клиенту
        """
        data_dto: GeoserviceSuggestionDataDTO = geoservice_dto.data

        suggestion_address_dto = SuggestionAddressDTO(dict(
            value=geoservice_dto.value,
            fias_id=data_dto.fias_id
        ))

        expected_accuracy = GeoPointsAccuracy.NEAREST.value

        if data_dto.qc_geo is not None and (
                data_dto.qc_geo <= expected_accuracy
        ):
            suggestion_address_dto.lat = data_dto.geo_lat
            suggestion_address_dto.lon = data_dto.geo_lon

        suggestion_address_dto.fias_level = FIAS_LEVEL_MAPPING.get(
            data_dto.fias_level, None
        )

        return suggestion_address_dto
