import logging

import requests
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets, mixins, status

from rest_framework.response import Response

from weather.filters import WeatherHistoryFilter
from weather.models import City, WeatherHistory
from weather.schemas import CITY_SCHEMA, WEATHER_HISTORY_SCHEMA, WEATHER_CITY_SCHEMA
from weather.serializers import (
    CitySerializer,
    WeatherHistorySerializer, WeatherSerializer,
)
from weather.services import get_weather_yandex


logger = logging.getLogger(__name__)


@extend_schema_view(**CITY_SCHEMA)
class CityViewset(viewsets.ModelViewSet):
    """Кастомный ViewSet для просмотра городов ."""

    queryset = City.objects.all()
    serializer_class = CitySerializer


@extend_schema_view(**WEATHER_HISTORY_SCHEMA)
class WeatherHistoryViewset(viewsets.ReadOnlyModelViewSet):
    """Кастомный ViewSet возвращает историю запросов."""

    queryset = WeatherHistory.objects.select_related("city").all()
    serializer_class = WeatherHistorySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = WeatherHistoryFilter
    ordering_fields = ("city__name", "request_type")
    ordering = ("city__name",)
    search_fields = ("city__name",)


@extend_schema_view(**WEATHER_CITY_SCHEMA)
class WeatherCityViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Получение данных о погоде по городу с API Яндекса ."""

    queryset = City.objects.all()
    serializer_class = WeatherSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("name",)

    def list(self, request, *args, **kwargs):
        """Получение по городу: температуры,
        атмосферное давление, скорость ветра"""

        # city_name = request.GET.get("city")
        city_name: str = request.GET.get("city",).title()
        if not city_name:
            return Response({
                "error": "Поле город обязательно для заполнения!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        city = get_object_or_404(City, name=city_name)

        try:
            response = self.get_serializer(get_weather_yandex(city)).data
        except Exception as e:
            return Response(
                {"error": f"Произошла ошибка по данному запросу: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(response)