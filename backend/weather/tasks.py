import logging
from celery import shared_task
from django.core.cache import cache

from weather.models import City, WeatherHistory
from weather.services import get_weather_yandex


@shared_task
def update_weather_data(city_id):
    """
    Обновляет данные о погоде для указанного города и сохраняет их в кэш.
    Данные кэшируются на 30 минут.
    Возвращает сообщение о результате операции.
    """

    city = City.objects.get(id=city_id)
    try:
        weather_data = get_weather_yandex(city)
        cache_key = f"weather_{city.name}"
        cache.set(cache_key, weather_data, timeout=60 * 30)
        return (f"Данные о погоде для {city.name}"
                f" кэширована с ключом '{cache_key}'"
                )

    except Exception as e:
        error_message = f"Ошибка при обновлении данных для города {city.name}: {str(e)}"
        print(error_message)
        return error_message