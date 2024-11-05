from django.contrib import admin

from .models import City


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
