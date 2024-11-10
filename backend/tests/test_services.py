# Запуск внутри контейнера отрабатывает успешно:
#tests/test_models.py ........                                                                                                             [ 44%]
#tests/test_services.py .                                                                                                                  [ 50%]
#tests/test_views.py .........                                                                                                             [100%]

#============================================================== 18 passed in 0.77s ===============================================================
#

import pytest
import unittest
from unittest.mock import patch, MagicMock
from weather.services import get_weather_yandex, local_weather_cache
from weather.models import City
from django.core.cache import cache


@pytest.mark.django_db
class TestGetWeatherYandex(unittest.TestCase):

    @patch("weather.services.requests.get")
    def test_get_weather_yandex_from_api(self, mock_get):
        """Тестирование получения данных о погоде через API Яндекса."""

        # Создание мок-ответа от API Яндекса
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "fact": {
                "temp": 20,
                "pressure_mm": 1015,
                "wind_speed": 5,
                "humidity": 80
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        city = City.objects.create(name="Москва")
        weather_data = get_weather_yandex(city)

        # Проверка, что данные были возвращены
        self.assertEqual(weather_data["temp"], 20)
        self.assertEqual(weather_data["pressure_mm"], 1015)
        self.assertEqual(weather_data["wind_speed"], 5)
        self.assertEqual(weather_data["humidity"], 80)

        self.assertIn("Москва", local_weather_cache)
        self.assertEqual(local_weather_cache["Москва"]["temp"], 20)

        cached_data = cache.get(f"weather_Москва")
        self.assertEqual(cached_data["temp"], 20)
