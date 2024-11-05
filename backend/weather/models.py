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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ("created",)



