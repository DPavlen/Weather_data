from drf_spectacular.utils import (extend_schema, OpenApiResponse, OpenApiParameter)


custom_city_schema = {"tags": ["city (Города)"]}
custom_weather_city_schema = {"tags": ["weather_city (Погода по городу API Yandex)"]}
custom_weather_history_schema = {"tags": ["weather_history (Истории запросов)"]}


CITY_SCHEMA = {
    "list": extend_schema(
        **custom_city_schema,
        summary="Получение списка всех городов ",
        description="Получение списка всех городов",
    ),
    "create": extend_schema(
        **custom_city_schema,
        summary="Создание нового города.",
        description="Создание нового города."
    ),
    "partial_update": extend_schema(
        **custom_city_schema,
        summary="Частичное обновление информации о городе. ",
        description="Частично обновляет информации о городе."
    ),
    "update": extend_schema(
        **custom_city_schema,
        summary="Полное обновление информации о городе. ",
        description="Полное обновление информации о городе."
    ),
    "destroy": extend_schema(
        **custom_city_schema,
        summary="Удаляет информацию от текущем городе.",
        description="УУдаляет информацию от текущем городе."
    ),
    "retrieve": extend_schema(
        **custom_city_schema,
        summary="Получить информацию о городе по ID.",
        description="Получить информацию о городе по ID. "
    ),
}


# Параметр limit_parameter
limit_parameter = OpenApiParameter(
    name="limit",
    type=int,
    location=OpenApiParameter.QUERY,
    required=False,
    description=(
        "Количество результатов на страницу (по умолчанию 10)."
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
        "Сортировка по полям: 'city__name' ; 'request_time' ; "
        " Добавьте префикс '-' для сортировки по убыванию. "
    ),
)

WEATHER_HISTORY_SCHEMA = {
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

# Параметр для указания города
city_parameter = OpenApiParameter(
    name="city",
    type=str,
    location=OpenApiParameter.QUERY,
    required=True,
    description="Введите город. Например Москва . "
)


WEATHER_CITY_SCHEMA = {

    "list": extend_schema(
        **custom_weather_city_schema,
        summary="Получить Погоду по городу API Yandex",
        description="Формат запроса: api/weather_city/?city=Москва"
                    " или api/weather_city/?city=москва",
        parameters=[
            city_parameter,
        ],
    ),
}
