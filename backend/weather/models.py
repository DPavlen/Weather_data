from django.db import models


class City(models.Model):
    """Модель городов."""

    name = models.CharField(
        "Название города",
        max_length=50,
        unique=True
    )
    latitude = models.DecimalField(
        "Широта",
        max_digits=9,
        decimal_places=6
    )
    longitude = models.DecimalField(
        "Долгота",
        max_digits=9,
        decimal_places=6
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания города",
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления города",
    )

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ("created",)

    def __str__(self):
        return self.name


class WeatherHistory(models.Model):
    """Модель истории запросов городов."""

    TYPE_CHOICES = (
        ("Web", "Веб"),
        ("Telegram", "Телеграм")
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name="Город"
    )
    request_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name="Тип запроса",
    )
    request_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время запроса города",
    )

    class Meta:
        verbose_name = "История запроса города"
        verbose_name_plural = "Истории запросов городов"
        ordering = ("request_time",)

    def __str__(self):
        return f"{self.city.name} - {self.request_time}"
