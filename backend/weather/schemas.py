from drf_spectacular.utils import (extend_schema, OpenApiResponse, OpenApiParameter)

custom_weather_history_schema = {"tags": ["requests (Истории запросов)"]}


# Параметр limit_parameter
limit_parameter = OpenApiParameter(
    name="limit",
    type=int,
    location=OpenApiParameter.QUERY,
    required=False,
    description=(
        "Количество результатов на страницу (по умолчанию 14)."
    ),
)
# Параметр offset_parameter
offset_parameter = OpenApiParameter(
    name="offset",
    type=int,
    location=OpenApiParameter.QUERY,
    required=False,
    description=(
        "Начальный индекс, начиная с которого возвращаются результаты."
    ),
)
# Параметр ordering_parameter для сортировки поля ordering
ordering_parameter = OpenApiParameter(
    name="ordering",
    type=str,
    location=OpenApiParameter.QUERY,
    required=False,
    description=(
        "Сортировка по полям: 'city' ; 'request_time' ; "
        " Добавьте префикс '-' для сортировки по убыванию. "
    ),
)


CUSTOM_WEATHER_HISTORY_SCHEMA = {
    "list": extend_schema(
        **custom_weather_history_schema,
        summary=" Получить список всех историй запросов по городам",
        description="Получить список всех историй запросов по городам",
        parameters=[
            limit_parameter,
            offset_parameter,
            ordering_parameter,
        ],
    ),
    "retrieve": extend_schema(
        **custom_weather_history_schema,
        summary="Получить информацию об истории запроса по ID. ",
        description="Получить информацию об истории запроса по ID "
    ),
}
