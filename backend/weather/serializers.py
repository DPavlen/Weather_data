from rest_framework import serializers
from weather.models import City, WeatherHistory


class CitySerializer(serializers.ModelSerializer):
    """Сериализатор для получения городов."""

    class Meta:
        model = City
        fields = ("id", "name", "latitude", "longitude")


class WeatherHistorySerializer(serializers.ModelSerializer):
    """Сериализатор для получения запросов по истории городов."""
    city = serializers.CharField(source="city.name", read_only=True)
    request_type = serializers.CharField(source="get_request_type_display")

    class Meta:
        model = WeatherHistory
        fields = ("id", "city", "request_type", "request_time")