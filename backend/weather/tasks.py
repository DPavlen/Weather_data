import logging
from celery import shared_task
from django.core.cache import cache

from weather.models import City, WeatherHistory
from weather.services import get_weather_yandex


@shared_task
def update_weather_data(city_id):
    city = City.objects.get(id=city_id)
    try:
        weather_data = get_weather_yandex(city)
        cache.set(f"weather_{city.name}", weather_data, timeout=60 * 30)
    except Exception as e:
        print(f"Ошибка при обновлении данных для города {city.name}: {str(e)}")