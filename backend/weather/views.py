from django_filters.filters import OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets, filters

from django.shortcuts import render
from rest_framework.filters import SearchFilter

from weather.filters import WeatherHistoryFilter
from weather.models import City, WeatherHistory
from weather.schemas import CUSTOM_WEATHER_HISTORY_SCHEMA
from weather.serializers import CitySerializer, WeatherHistorySerializer


class CityViewset(viewsets.ReadOnlyModelViewSet):
    """Кастомный ViewSet для просмотра городов ."""

    queryset = City.objects.all()
    serializer_class = CitySerializer


@extend_schema_view(**CUSTOM_WEATHER_HISTORY_SCHEMA)
class WeatherHistoryViewset(viewsets.ReadOnlyModelViewSet):
    """Кастомный ViewSet возвращает историю запросов."""

    queryset = WeatherHistory.objects.all()
    serializer_class = WeatherHistorySerializer
    ordering_fields = ("city", "request_time")
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = WeatherHistoryFilter


