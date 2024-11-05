import json

from django.core.management.base import BaseCommand
from weather.models import City


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            with open("data/city.json", encoding="utf-8-sig") as f:
                city_data = json.load(f)
                for city in city_data:
                    name = city.get("name")
                    latitude = city.get("latitude")
                    longitude = city.get("longitude")
                    City.objects.get_or_create(
                        name=name,
                        latitude=latitude,
                        longitude=longitude
                    )
        except City.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "Ошибка: "))
        return (
            "Загрузка 'Городов с широтой и долготой' произошла успешно!"
            " Обработка файла city.json завершена."
        )