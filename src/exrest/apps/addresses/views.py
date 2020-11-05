from copy import copy

from django.db import transaction
from django.db.transaction import on_commit
from django_filters import FilterSet, BaseInFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from exrest.apps.addresses.dto import SuggestionAddressParamsDTO
from exrest.apps.addresses.enums import AddressTypeEnum
from exrest.apps.addresses.models import Address
from exrest.apps.addresses.serializers import (
    AddressSerializer, SuggestionsRequestSerializer,
    SuggestionsResponseSerializer, ReverseGeocodingRequestSerializer,
    ReverseGeocodingResponseSerializer)
from exrest.apps.addresses.use_cases import GetAddressesSuggestionsUseCase
from exrest.apps.background_tasks.tasks import update_coordinates_task
from exrest.apps.background_tasks.utils import irrelevant_address_coordinates
from exrest.apps.comments.enums import CommentObjectTypeChoices
from exrest.apps.comments.serializers import (
    SendCommentRequestSerializer, CommentSerializer)
from exrest.apps.comments.utils import create_comment
from exrest.apps.geo.gateways import GeoserviceGateway
from exrest.apps.notifications.di import clients_notifier
from exrest.apps.notifications.events import UpdateAddressEvent
from exrest.common.exceptions import ExternalServiceError


class AddressFilter(FilterSet):
    """Фильтры для AddressViewSet.

    Добавляет фильтрацию по списку id.
    """

    ids = BaseInFilter(field_name='id')

    class Meta:
        model = Address
        fields = ('id', 'ids', )


class AddressViewSet(ModelViewSet):
    """ViewSet адресов."""

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (ActionPermission,)
    # permissions = AddressesPermissionGenerator
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    pagination_class = LimitOffsetPagination
    filter_class = AddressFilter

    @swagger_auto_schema(
        query_serializer=SuggestionsRequestSerializer,
        responses={200: SuggestionsResponseSerializer}
    )
    @action(detail=False, methods=('get',))
    def suggestions(self, request):
        """Эндпоинт на получение подсказок адресов."""
        # Копируем все параметры запроса
        params = copy(request.query_params)

        # извлекаем тип - его нужно ремапить
        object_type = params.get('type')

        params['from_bound'] = params['to_bound'] = object_type

        # В системе под городом подразумевается любой населенный пукт
        # поэтому необходимо расширить границы поиска.
        if object_type == AddressTypeEnum.CITY:
            params['to_bound'] = AddressTypeEnum.SETTLEMENT.value

        search_address_dto = SuggestionAddressParamsDTO(params)

        try:
            suggestions = GetAddressesSuggestionsUseCase.execute(
                search_address_dto
            )

            response = Response(suggestions.to_primitive())
        except ExternalServiceError as err:
            response = Response(
                data={
                    'errors': [err.args[0]],
                    'message': 'Не удалось получить подсказку по адресу',
                    'status': '400'
                },
                status=400
            )

        return response

    @swagger_auto_schema(
        query_serializer=ReverseGeocodingRequestSerializer,
        responses={200: ReverseGeocodingResponseSerializer}
    )
    @action(detail=False, methods=('get',))
    def geocoding(self, request):
        """Эндпоинт для геокодирования адреса."""
        try:
            geoservice_response = GeoserviceGateway().get_coords_by_address(
                request.query_params['query']
            )

            response = Response(geoservice_response)
        except ExternalServiceError as err:
            response = Response(
                data={
                    'errors': [err.args[0]],
                    'message': 'Не удалось получить координаты адреса',
                    'status': '400'
                },
                status=400
            )

        return response

    @swagger_auto_schema(
        request_body=SendCommentRequestSerializer,
        responses={200: CommentSerializer}
    )
    @action(detail=True, methods=('post',))
    def comment(self, request, pk=None):
        """Эндпоинт на отправку комментария к адресу."""
        return create_comment(
            request, pk, CommentObjectTypeChoices.ADDRESS, Address
        )

    @transaction.atomic
    def perform_update(self, serializer):
        new_address = serializer.save()

        if irrelevant_address_coordinates(
            self.request.data, serializer.instance
        ):
            on_commit(
                lambda: update_coordinates_task.delay(
                    address_ids=[new_address.id]
                )
            )

        # эвент на изменение адреса клиента.
        event = UpdateAddressEvent(address_id=self.kwargs['pk'])
        clients_notifier.fire(event)
