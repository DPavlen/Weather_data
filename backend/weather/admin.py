from django.contrib import admin

from .models import City, WeatherHistory


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления городами."""

    list_display = (
        "id",
        "name",
        "latitude",
        "longitude",
        "created",
        "updated"
    )
    list_display_links = ("id", "name")
    search_fields = ("name",)
    empty_value_display = "-пусто-"


@admin.register(WeatherHistory)
class WeatherHistoryAdmin(admin.ModelAdmin):
    """Административный интерфейс для
    управления историей о запросах по городам."""

    list_display = (
        "id",
        "city",
        "request_time",
        "request_type",
    )
    list_display_links = ("id", "city")
    search_fields = ("request_type",)
    empty_value_display = "-пусто-"