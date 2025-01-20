# Weather_data

## 1. [Описание проекта ](#1)
## 2. [Функционал API, эндпойнты и технические особенности](#2)
## 3. [Стек технологий](#3)
## 4. [Запуск проекта через docker compose и ссыылка на него](#4)
## 5. [Автор проекта:](#5)
#######fewfwefwefwefefwef
## 1. Описание проекта <a id=1></a>

__API для прогноза погоды:__
- Эндпоинт GET /weather?city=<city_name> возвращает текущую температуру, 
давление и скорость ветра в городе <city_name> (на русском). 
- При первом запросе данные берутся с сервиса Yandex; 
повторные запросы в течение 30 минут обслуживаются кэшированными данными.
- Эндпоинт GET /requests предоставляет историю запросов с возможностью фильтрации 
по типу запроса (web, telegram), сортировки и пагинации.
- CRUD-операции для городов доступны по эндпоинтам /cities и /cities/<id>, с поддержкой пагинации.
- 
__Telegram-бот:__
- Бот с кнопкой "Узнать погоду", которая запрашивает у пользователя название города и 
возвращает прогноз на сегодняшний день.
- 
__Тестирование:__
- Написание тестов для всех ключевых функций проекта.

## 2. Функционал API, эндпойнты и технические особенности. Телеграмм бот. <a id=2></a>

__Создан загрузчик python manage.py add_user и 2 суперпользователя для административной панели__
__Написана COLLECT_SCHEMA для документирования эндпойнтов.__
- http://localhost:8000/api/swagger/ реализована возможность автоматической генерации документации для API, с помощью Swagger
- https://localhost:8000/api/redoc/ реализована возможность автоматической генерации документации для API, с помощью Redoc\
__Создан загрузчик для городов python manage.py add_city, по которым будем получать погоду.__\
__Реализована работа с city (Города). CRUD запросы для работы с городами.__
<details>
    <summary>Реализована работа с city (Города)</summary>
    <ul>
     <li> - http://localhost:8000/api/city/ GET-list. Получить список всех городов</li> 
     <li> - http://localhost:8000/api/city/ POST-create. Создание нового города.</li>
     <li> - http://localhost:8000/api/city/{id} GET-retrieve. Получить информацию о городе по ID.</li> 
     <li> - http://localhost:8000/api/cats/{id} PUT-update. Полное обновление информации о городе по ID.</li> 
     <li> - http://localhost:8000/api/cats/{id} PATCH-partial_update. Изменение информации о городе по ID.</li> 
     <li> - http://localhost:8000/api/city/{id} DELETE-destroy. Удаление информации о котенке.</li> 
    </ul>
</details>

__Реализована работа c weather_city (Погода по городу API Yandex)"__
- http://127.0.0.1:8000/api/weather_city/?city=Москва GET-list. Где на вход необходимо подать название города. 
Получение данных о погоде по городу с API Яндекса. Данные: температуры, атмосферное давление, скорость ветра, влажность.
Также реализовано кэширование запроса. 
- Асинхронная обработка задачи(task): Обновляет данные о погоде для указанного города и сохраняет их в кэш.
Данные кэшируются на 30 минут (Используется Celery + Redis).Мониторинг Celery задач осуществляется с помощью Flower.

__Реализована работа c weather_history (Истории запросов)__\
- http://localhost:8000/api/weather_history/ GET-list. Получить список всех историй запросов по городам.\
Сортировка по полям: Город, дата ; Добавьте префикс '-' для сортировки по убыванию.\
Реализован фильтр по типу запроса(web, telegram), например 'te', получим все запросы с типом: Телеграм.\
Реализована пагинация. 
- http://localhost:8000/api/weather_history/{id} GET-retrieve. Получить истори информации о городе по ID.

__Реализован телеграм бота, который после нажатия кнопки "Узнать погоду", требует Введите название города.__\
Далее вводим например город: Казань и получаем ответ в формате:
- Сегодня 10.11.2024
- Погода в Казань:
- Температура: 2°C
- Атмосферное давление: 760 мм рт. ст.
- Скорость ветра: 3.1 м/с
- Влажность: 78%

Примеры работы приложения Django-API and Telegram-bota.
![image](https://github.com/user-attachments/assets/fe7bf9a0-a0cc-4a98-bd79-0052065acbb5)
![image](https://github.com/user-attachments/assets/19aef3af-4e66-4b1f-8491-90fb6d2cf271)
![image](https://github.com/user-attachments/assets/3df4a7ad-720e-4e28-ada9-5ef016416778)
![image](https://github.com/user-attachments/assets/e2246f9b-e64b-4b4a-bc3b-b7dbf96fdcbf)
![image](https://github.com/user-attachments/assets/fb1b88d1-abe0-4015-bf38-dbd5bc96a6cb)
![image](https://github.com/user-attachments/assets/31ae7a4a-595c-41bb-b4d9-ac82ed1f976a)
![image](https://github.com/user-attachments/assets/e9ab0c43-e130-48d0-a296-3e87404a4433)



## 3. Стек технологий <a id=3></a>
[![Django](https://img.shields.io/badge/Django-5.0.2-6495ED)](https://www.djangoproject.com) 
[![Djangorestframework](https://img.shields.io/badge/djangorestframework-3.14.0-6495ED)](https://www.django-rest-framework.org/) 
[![Nginx](https://img.shields.io/badge/Nginx-1.21.3-green)](https://nginx.org/ru/)  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/)
[![Celery](https://img.shields.io/badge/Celery-%205.2.7-blue?style=flat-square&logo=celery)](https://docs.celeryq.dev/en/stable/)
[![Redis](https://img.shields.io/badge/Redis-%205.0.7-ff6600?style=flat-square&logo=redis)](https://redis.io/)
[![Flower](https://img.shields.io/badge/Flower-mher/flower:0.9.7-FF69B4?style=flat-square&logo=flower)](https://flower.readthedocs.io/en/latest/)
[![Swagger](https://img.shields.io/badge/Swagger-%201.21.7-blue?style=flat-square&logo=swagger)](https://swagger.io/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-%2020.0.4-blue?style=flat-square&logo=gunicorn)](https://gunicorn.org/) 
[![Docker](https://img.shields.io/badge/Docker-%2024.0.5-blue?style=flat-square&logo=docker)](https://www.docker.com/)
[![DockerCompose](https://img.shields.io/badge/Docker_Compose-%202.21.0-blue?style=flat-square&logo=docsdotrs)](https://docs.docker.com/compose/)
[![Tested with pytest](https://img.shields.io/badge/Tested_with_pytest-8.1.1-6495ED)](https://docs.pytest.org/en/8.1.x/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.14.0-6495ED)](https://aiogram.dev/)


## 4. Запуск проекта через docker compose и ссылка на него <a id=4></a>
## Запуск проекта локально в Docker-контейнерах с помощью Docker Compose

Склонируйте проект из репозитория:

```shell
git clone git@github.com:DPavlen/Weather_data.git
```

Перейдите в директорию проекта:

```shell
cd Weather_data/
```
Ознакомьтесь с .env.example и после этого перейдите в  
корень директории **Weather_data/** и создайте файл **.env**:

```shell
nano .env
```

Добавьте строки, содержащиеся в файле **.env.example** и подставьте 
свои значения.

Пример из .env файла:

```dotenv
SECRET_KEY=DJANGO_SECRET_KEY        # Ваш секретный ключ Django
DEBUG=False                         # True - включить Дебаг. Или оставьте пустым для False
IS_LOGGING=False                    # True - включить Логирование. Или оставьте пустым для False
ALLOWED_HOSTS=127.0.0.1 backend     # Список адресов, разделенных пробелами


# Помните, если вы выставляете DEBUG=False, то необходимо будет настроить список ALLOWED_HOSTS.
# 127.0.0.1 и backend является стандартным значением. Через пробел.
# Присутствие backend в ALLOWED_HOSTS обязательно.

В зависимости какую БД нужно запустит:
#DB_ENGINE=sqlite3
DB_ENGINE=postgresql

POSTGRES_USER=django_user                  # Ваше имя пользователя для бд
POSTGRES_PASSWORD=django                   # Ваш пароль для бд
POSTGRES_DB=django                         # Название вашей бд
DB_HOST=db                                 # Стандартное значение - db
DB_PORT=5432                               # Стандартное значение - 5432

DEBUG=True
ALLOWED_HOSTS=127.0.0.1 localhost
CORS_ALLOWED_ORIGINS=http://127.0.0.1:5173 http://localhost:5173
CSRF='http://localhost:5173'

YANDEX_API_WEATHER_KEY=XXXXXXXX-YYYY-ZZZZ-XXXX-EEEEEEEEEEEE # Api key от сервиса Яндекс.Погоды
YANDEX_WEATHER_URL=https://api.weather.yandex.ru/v2/forecast/ # URL APi  от сервиса Яндекс.Погоды

CELERY_BROKER_URL = 'redis://redis:6379/0'

TELEGRAM_BOT_TOKEN=XXWWWXXWXXWXWX    # Токен телеграмм бота
ADMIN_CHAT_ID=RRRRRRRR               # ID Chat телеграмм бота из которого делается Бот
WEATHER_API_URL="http://localhost:8000/api/weather_city/"  # API Django откуда Бот забирает информацию


```

```shell
В директории **docker** проекта находится файл **docker-compose.yml**, с 
помощью которого вы можете запустить проект локально в Docker контейнерах.
```

Находясь в директории **Weather_data/** выполните следующую команду:
```shell
sudo docker compose -f docker-compose.yml up --build
```

> **Примечание.** Если нужно - добавьте в конец команды флаг **-d** для запуска
> в фоновом режиме. У нас сбилдится сеть: weather_data, состоящий из Docker-контейнеров: 
> weather_data-flower-1, weather_data-nginx-1 , weather_data-bot-1, weather_data-backend-1

> **Примечание.** Также создатся суперпользователь для Django-админки: 
> "username": "admin", "password": "1"

> **Примечание.** Что запустить автотесты: нам необходимо провалиться внутрь контейнера
> weather_data-backend-1, т.е. выполнить команду:
```shell
sudo docker exec -it weather_data-backend-1 /bin/bash
```
```shell
И далее внутри контейнера :/app# pytest
Пример вывода при успешном выполнении тестов:
tests/test_models.py ........                                                                                                             [ 38%]
tests/test_serializers.py ...                                                                                                             [ 52%]
tests/test_services.py .                                                                                                                  [ 57%]
tests/test_views.py .........                                                                                                             [100%]
============================================================== 21 passed in 1.65s ===============================================================
```

>**Примечание.** Запускаем собраный уже ранее командой:
```shell      
sudo docker compose -f docker-compose.yml up -d**
```

>**Примечание.** Для того чтобы необходимо остановить и удалить контейнер нужно использовать:   
```shell
sudo docker compose -f docker-compose.yml down 
```

По завершении всех операции проект будет запущен и доступен по адресу
http://127.0.0.1/ или http://localhost/ в зависимости от настроек

Либо просто завершите работу Docker Compose в терминале, в котором вы его
запускали, сочетанием клавиш **CTRL+C**.

***


```shell
sudo docker compose -f docker-compose.yml up --build
```

>**Примечание.** Запускаем собраный уже ранее командой:
```shell      
sudo docker compose -f docker-compose.yml up -d**
```

>**Примечание.** Для того чтобы необходимо остановить и удалить контейнер нужно использовать:   
```shell
sudo docker compose -f docker-compose.yml down 
```

По завершении всех операции проект будет запущен и доступен по адресу
http://127.0.0.1/ или http://localhost/ в зависимости от настроек

Либо просто завершите работу Docker Compose в терминале, в котором вы его
запускали, сочетанием клавиш **CTRL+C**.

***

## 5. Автор проекта: <a id=5></a> 
**Павленко Дмитрий**  
- Ссылка на мой профиль в GitHub [Dmitry Pavlenko](https://github.com/DPavlen)  
