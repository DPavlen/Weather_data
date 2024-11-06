from django.urls import include, path
from rest_framework import routers

from weather.views import CityViewset, WeatherHistoryViewset

router = routers.DefaultRouter()
router.register(r"city", CityViewset, basename="city")
router.register(r"requests", WeatherHistoryViewset, basename="requests")


urlpatterns = [
    path("", include(router.urls)),
    ]