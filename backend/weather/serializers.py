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


class WeatherSerializer(serializers.Serializer):
    """Сериализатор, склеивающий City+YANDEX_API."""

    city_name = serializers.CharField()
    temp = serializers.IntegerField()
    pressure_mm = serializers.IntegerField()
    wind_speed = serializers.FloatField()
    humidity = serializers.IntegerField()

    class Meta:
        model = City
        fields = ("city_name", "temp", "pressure_mm", "wind_speed", "humidity")

    def to_representation(self, instance):
        """Вывод представления в читабельном виде."""

        representation = super().to_representation(instance)
        return {
            "Город": representation["city_name"],
            "Температура в °C": representation["temp"],
            "Атмосферное давление (мм рт.ст.)": representation["pressure_mm"],
            "Скорость ветра (м/с)": representation["wind_speed"],
            "Влажность (в процентах)": representation["humidity"]
        }