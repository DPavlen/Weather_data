from decimal import Decimal

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from weather.models import (
    City,
    WeatherHistory
)
from weather.pagination import PaginationCust


class TestCityViewset(APITestCase):
    """
    Тесты для проверки функциональности городов.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Установка начальных данных для всех тестов в классе.
        Этот метод вызывается один раз для установки данных, которые будут
        использоваться всеми тестовыми методами в данном классе.
        """
        cls.city_one = City.objects.create(
            name="Test_Москва",
        )
        cls.city_two = City.objects.create(
            name="Test_Санкт-Петербург",
        )

    def setUp(self):
        """
        Создаёт экземпляр APIClient, который будет использоваться для выполнения
        HTTP-запросов в тестах.
        """
        self.client = APIClient()

    def get_authenticated_client(self):
        """
        Возвращает клиент для любого пользователя, без аутентификации.
        """

        return self.client

    def test_city_list(self):
        """
        Тест для получения списка городов.
        GET-запрос "city_list" и ответ - 200 OK.
        """
        url = reverse("city-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["name"], self.city_one.name)

    def test_city_detail(self):
        """
        Тест для получения деталей конкретного города.
        GET-запрос "city-detail" с ID города и ответ - 200 OK.
        """

        url = reverse("city-detail", kwargs={"pk": self.city_two.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_city_create(self):
        """
        Тест для создания города.
        POST-запрос на создание города и проверка ответа.
        """

        url = reverse("city-list")
        data = {
                "name": "Test_Казань",
                "latitude": 55.7558,
                "longitude": 37.6173
            }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["name"], "Test_Казань")

    def test_city_create(self):
        """
        Тест для удаления города.
        POST-запрос на создание города и проверка ответа.
        """

        url = reverse("city-list")
        data = {
                "name": "Test_Казань",
                "latitude": 55.7558,
                "longitude": 37.6173
            }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["name"], "Test_Казань")

    def test_city_delete(self):
        """
        Тест для удаления города.
        DELETE-запрос на удаление города и проверка ответа.
        Сначала создаем город, а потом удаляем .
        """

        url = reverse("city-list")
        data = {
            "name": "Test_Екатеринбург",
            "latitude": 0,
            "longitude": 0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        city_id = response.data["id"]
        delete_url = reverse("city-detail", kwargs={"pk": city_id})
        delete_response = self.client.delete(delete_url)

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        get_response = self.client.get(delete_url)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_city_partial_update(self):
        """
        Тест для частичного обновления данных города.
        PATCH-запрос на обновление только одного поля (например, latitude).
        """

        url = reverse("city-detail", kwargs={"pk": self.city_one.id})
        partial_data = {
            "latitude": 55.999800
        }
        response = self.client.patch(url, partial_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что обновилось только поле latitude
        self.city_one.refresh_from_db()
        self.assertEqual(self.city_one.latitude, Decimal("55.9998"))
        self.assertEqual(self.city_one.name, "Test_Москва")


class WeatherHistoryViewset(APITestCase):
    """
    Тесты для проверки функциональности истории запросов городов.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Установка начальных данных для всех тестов в классе.
        Этот метод вызывается один раз для установки данных,
        которые будут использоваться всеми тестовыми методами
        в данном классе.
        """
        cls.city_one = City.objects.create(name="Test_Москва")
        cls.weather_history_one = WeatherHistory.objects.create(
            city=cls.city_one,
            request_type="Web",
        )
        cls.city_two = City.objects.create(name="Test_Санкт-Петербург",)
        cls.weather_history_two = WeatherHistory.objects.create(
            city=cls.city_two,
            request_type="Telegram",
        )
        cls.url = reverse("weather_history-list")

    def setUp(self):
        """
        Создаёт экземпляр APIClient, который будет использоваться для выполнения
        HTTP-запросов в тестах.
        """
        self.client = APIClient()

    def get_authenticated_client(self):
        """
        Возвращает клиент для любого пользователя, без аутентификации.
        """

        return self.client

    def test_weather_history_list(self):
        """
        Тест для получения истории запросов городов.
        GET-запрос "weather_history-list" и ответ - 200 OK.
        """
        url = reverse("weather_history-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["city"],
                         self.weather_history_one.city.name)

    def test_weather_history_detail(self):
        """
        Тест для получения деталей конкретного запроса истории города.
        GET-запрос "weather_history-detail" с ID города и ответ - 200 OK.
        """

        url = reverse("weather_history-detail",
                      kwargs={"pk": self.weather_history_two.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_weather_history_by_city_name(self):
        """Тест для поиска по названию города в истории погоды."""

        response = self.client.get(self.url, {"search": "Москва"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) > 0)

        # Проверка "results" по полю city содержит "Москва"
        for item in response.data["results"]:
            self.assertIn("Москва", item["city"])

    def test_ordering_weather_history_by_request_type_desc(self):
        """Тест сортировку истории погоды по типу запроса в убывающем порядке."""

        response = self.client.get(self.url, {"ordering": "request_type"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = [item["request_type"] for item in response.data["results"]]
        self.assertEqual(results, sorted(results, reverse=True))

