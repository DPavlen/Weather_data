import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import (
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    PositiveSmallIntegerField
)
from django.test import TestCase
from gunicorn.config import User
from pytest import mark
from pytest_django.asserts import assertRaisesMessage


from weather.models import (
    City,
    WeatherHistory
)


@mark.django_db
class TestCityModel(TestCase):
    """Тесты для модели City(Города)."""

    def test_str_representation(self):
        """
        Проверка строкового представления модели City.
        """
        city = City.objects.create(name="Test_Москва")
        assert str(city) == "Test_Москва"

    def test_non_essential_field(self):
        """
        Проверка необязательных пустых полей.
        """
        city = City.objects.create(latitude=None, longitude=None)
        assert city.latitude is None
        assert city.longitude is None

    def test_auto_fill_dates_fields(self):
        """Проверка автозаполнения дат."""
        city = City.objects.create(latitude=0.0, longitude=0.0)

        now = timezone.now()
        self.assertIsNotNone(city.created)
        self.assertIsNotNone(city.updated)
        self.assertTrue(city.created <= city.updated)
        self.assertTrue(
            abs(now - city.created).total_seconds() < 5)
        self.assertTrue(
            abs(now - city.updated).total_seconds() < 5)
        city.save()
        self.assertNotEqual(city.created, city.updated)

    def test_models_fields(self):
        """
        Проверка полей модели City.
        """
        fields = City._meta.fields
        fields_names = [field.name for field in fields]
        assert "name" in fields_names
        assert "latitude" in fields_names
        assert "longitude" in fields_names
        assert "created" in fields_names
        assert "updated" in fields_names

    def test_fields_types(self):
        """
        Проверка типов данных полей модели City.
        """
        assert isinstance(City._meta.get_field("name"), CharField)
        assert isinstance(City._meta.get_field("latitude"), DecimalField)
        assert isinstance(City._meta.get_field("longitude"), DecimalField)
        assert isinstance(City._meta.get_field("created"), DateTimeField)
        assert isinstance(City._meta.get_field("updated"), DateTimeField)


@mark.django_db
class TestWeatherHistoryModel(TestCase):
    """Тесты для модели WeatherHistory
    (Истории запросов городов)."""

    def test_str_representation(self):
        """
        Проверка строкового представления модели WeatherHistory.
        """
        city = City.objects.create(name="Test_Москва")
        weather_history = WeatherHistory.objects.create(
            city=city,
            request_type="Web",
        )
        self.assertEqual(str(weather_history), "Test_Москва - Web")

    def test_models_fields(self):
        """
        Проверка полей модели City.
        """
        fields = WeatherHistory._meta.fields
        fields_names = [field.name for field in fields]
        assert "city" in fields_names
        assert "request_type" in fields_names
        assert "request_time" in fields_names

    def test_fields_types(self):
        """
        Проверка типов данных полей модели City.
        """
        assert isinstance(WeatherHistory._meta.get_field("city"), ForeignKey)
        assert isinstance(WeatherHistory._meta.get_field("request_type"), CharField)
        assert isinstance(WeatherHistory._meta.get_field("request_time"), DateTimeField)