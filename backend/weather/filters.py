import django_filters
from django_filters import rest_framework as filters

from weather.models import WeatherHistory


class WeatherHistoryFilter(filters.FilterSet):
    """
    Фильтрация по имени специализации.
    """

    request_type = filters.CharFilter(
        field_name="request_type",
        lookup_expr="istartswith",
        label="Название Типа запроса",
        help_text="Введите тип запроса(web, telegram), например 'te', "
                  "получим все запросы с типом: Телеграм."
    )

    class Meta:
        model = WeatherHistory
        fields = ("request_type",)
