from django.urls import include, path
from rest_framework import routers

from weather.views import (
    CityViewset,
    WeatherHistoryViewset,
    WeatherCityViewset
)

router = routers.DefaultRouter()
router.register(r"city", CityViewset, basename="city")
router.register(r"weather_history", WeatherHistoryViewset, basename="weather_history")
router.register(r"weather_city", WeatherCityViewset, basename="weather_city")


urlpatterns = [
    path("", include(router.urls)),
    ]