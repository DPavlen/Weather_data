import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from pathlib import Path


class Command(BaseCommand):
    help = "Создание пользователей из JSON-файла"

    def handle(self, *args, **options) -> str | None:

        file_path = Path("data/user.json")
        if not file_path.is_file():
            self.stdout.write(self.style.ERROR("JSON файл не найден"))
            return

        with open(file_path, "r", encoding="utf-8") as file:
            users = json.load(file)

        for user_data in users:
            username = user_data.get("username")
            email = user_data.get("email")
            password = user_data.get("password")

            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Создан суперпользователь {username}")
                )
            else:
                self.stdout.write(
                    f"Пользователь с именем пользователя {username} уже существует"
                )
        return ("Загрузка 'Суперпользоватлей' произошла успешно!"
                " Обработка файла user.json завершена."
            )