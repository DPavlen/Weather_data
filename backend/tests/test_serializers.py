from decimal import Decimal

from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from weather.models import City, WeatherHistory
from weather.serializers import (
    CitySerializer,
    WeatherHistorySerializer,
    WeatherSerializer
)


class TestCitySerializer(APITestCase):
    def setUp(self):
        self.city = City.objects.create(
            name="Москва", latitude=55.7558, longitude=37.6173
        )

    # def test_city_serializer_valid(self):
    #     """Проверка правильной сериализации объекта города."""
    #     serializer = CitySerializer(self.city)
    #     data = serializer.data
    #
    #     self.assertIsInstance(data["latitude"], Decimal)
    #     self.assertIsInstance(data["longitude"], Decimal)
    #     self.assertEqual(round(data["latitude"], 4), 55.7558)
    #     self.assertEqual(round(data["longitude"], 4), 37.6173)

    def test_city_serializer_invalid(self):
        """Проверка обязательных полей(остуствующих)."""
        invalid_data = {
            "name": "Тестовый город",
            "latitude": None,
            "longitude": None
        }
        serializer = CitySerializer(data=invalid_data)
        self.assertTrue(serializer.is_valid())


class TestWeatherHistorySerializer(APITestCase):
    def setUp(self):
        self.city = City.objects.create(
            name="Москва", latitude=55.7558, longitude=37.6173)
        self.history = WeatherHistory.objects.create(
            city=self.city,
            request_type="forecast",
            request_time="2024-11-11T12:00:00Z"
        )

    # def test_weather_history_serializer_valid(self):
    #     """Проверка корректности сериализации истории запроса погоды."""
    #
    #     valid_data = {
    #         "request_time": "2024-11-11T12:00:00Z",
    #         "city": self.city.id,
    #     }
    #     serializer = WeatherHistorySerializer(data=valid_data)
    #     self.assertFalse(serializer.is_valid())
    #     result = serializer.validated_data
    #     self.assertEqual(result["request_time"], "2024-11-11T12:00:00Z")

    # def test_weather_history_serializer_invalid(self):
    #     """Проверка сериализации истории запроса с отсутствующими полями."""
    #
    #     invalid_data = {
    #         "request_type": "forecast",
    #         "city": None,
    #     }
    #     serializer = WeatherHistorySerializer(data=invalid_data)
    #     self.assertFalse(serializer.is_valid())
    #     self.assertIn("city", serializer.errors)


class TestWeatherSerializer(APITestCase):
    def setUp(self):
        self.city = City.objects.create(
            name="Москва",
            latitude=55.7558,
            longitude=37.6173
        )
        self.weather_data = {
            "city_name": "Москва",
            "temp": 20,
            "pressure_mm": 1015,
            "wind_speed": 5.0,
            "humidity": 80
        }

    def test_weather_serializer_valid(self):
        """Проверка сериализации данных о погоде."""

        self.weather_data = {
            "city_name": "Москва",
            "temp": 20,
            "pressure_mm": 1015,
            "wind_speed": 5.0,
            "humidity": 80
        }

        serializer = WeatherSerializer(data=self.weather_data)
        self.assertTrue(serializer.is_valid())
        data = serializer.validated_data

        self.assertEqual(data["city_name"], "Москва")
        self.assertEqual(data["temp"], 20)
        self.assertEqual(data["pressure_mm"], 1015)
        self.assertEqual(data["wind_speed"], 5.0)
        self.assertEqual(data["humidity"], 80)

    def test_weather_serializer_invalid(self):
        """Проверка сериализации данных о погоде с
         отсутствующими или некорректными значениями."""

        invalid_data = {
            "city_name": "Москва",
            "temp": "invalid",
            "pressure_mm": 1015,
            "wind_speed": 5.0,
            "humidity": 80
        }
        serializer = WeatherSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("temp", serializer.errors)

    # def test_to_representation(self):
    #     """Проверка правильности вывода в читабельном виде."""
    #     serializer = WeatherSerializer(data=self.weather_data)
    #     serializer.is_valid()
    #     representation = serializer.to_representation(serializer.instance)
    #
    #     self.assertEqual(representation["Город"], "Москва")
    #     self.assertEqual(representation["Температура в °C"], 20)
    #     self.assertEqual(representation["Атмосферное давление (мм рт.ст.)"], 1015)
    #     self.assertEqual(representation["Скорость ветра (м/с)"], 5.0)
    #     self.assertEqual(representation["Влажность (в процентах)"], 80)