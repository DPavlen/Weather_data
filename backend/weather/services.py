from typing import Dict, Any, Union
import requests
from backend.settings import YANDEX_API_WEATHER_KEY, YANDEX_WEATHER_URL
from weather.models import City


def get_weather_yandex(city: City) -> Dict[str, Union[str, int]]:
    """Получает данные о погоде для города через API Яндекса.."""

    headers = {
        "X-Yandex-Weather-Key": YANDEX_API_WEATHER_KEY,
    }
    params: Dict[str, Union[str, float]] = {
        "lat": city.latitude,
        "lon": city.longitude,
    }
    # Запрос о погоде
    response = requests.get(YANDEX_WEATHER_URL, headers=headers, params=params)
    response.raise_for_status()

    # Парсинг данных о погоде. Объект "fact" из ответа API Яндекса
    data: Dict[str, Union[str, int]] = response.json().get("fact")
    weather_data: Dict[str, Union[str, int]] = parse_data(data)
    weather_data["city_name"] = city.name

    return weather_data


def parse_data(data: Dict[str, Any]) -> Dict[str, Union[str, int]]:
    """Парсим данные о погоде c API."""

    weather_fields = ["temp", "pressure_mm", "wind_speed", "humidity"]
    return {key: data.get(key) for key in weather_fields}