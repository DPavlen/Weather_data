import logging
from datetime import timezone

import requests
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny

from rest_framework.response import Response

from weather.filters import WeatherHistoryFilter
from weather.models import City, WeatherHistory
from weather.pagination import PaginationCust
from weather.schemas import CITY_SCHEMA, WEATHER_HISTORY_SCHEMA, WEATHER_CITY_SCHEMA
from weather.serializers import (
    CitySerializer,
    WeatherHistorySerializer, WeatherSerializer,
)
from weather.services import get_weather_yandex
from weather.tasks import update_weather_data


logger = logging.getLogger(__name__)


@extend_schema_view(**CITY_SCHEMA)
class CityViewset(viewsets.ModelViewSet):
    """Кастомный ViewSet для просмотра городов ."""

    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = PaginationCust
    permission_classes = (AllowAny,)


@extend_schema_view(**WEATHER_HISTORY_SCHEMA)
class WeatherHistoryViewset(viewsets.ReadOnlyModelViewSet):
    """Кастомный ViewSet возвращает историю запросов."""

    queryset = WeatherHistory.objects.select_related("city").all()
    serializer_class = WeatherHistorySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = WeatherHistoryFilter
    ordering_fields = ("city__name", "request_type")
    search_fields = ("city__name",)
    pagination_class = PaginationCust


@extend_schema_view(**WEATHER_CITY_SCHEMA)
class WeatherCityViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Получение данных о погоде по городу с API Яндекса ."""

    queryset = City.objects.all()
    serializer_class = WeatherSerializer

    def list(self, request, *args, **kwargs):
        """Получение по городу: температуры,
        атмосферное давление, скорость ветра, влажность"""

        city_name: str = request.GET.get("city",).title()
        if not city_name:
            return Response({
                "error": "Поле город обязательно для заполнения!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        city = get_object_or_404(City, name=city_name)

        # Определяем тип запроса (например, по умолчанию "Web")
        request_type = "Web" if request.user.is_authenticated else "Telegram"

        # Создаем запись в истории запросов
        WeatherHistory.objects.create(
            city=city,
            request_type=request_type,
        )

        cached_data = cache.get(f"weather_{city_name}")
        if cached_data:
            return Response(cached_data)

        update_weather_data.delay(city.id)
        try:
            response = self.get_serializer(get_weather_yandex(city)).data
        except Exception as e:
            return Response(
                {"error": f"Произошла ошибка по данному запросу: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(response)