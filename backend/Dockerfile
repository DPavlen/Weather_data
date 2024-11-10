FROM python:3.11.9-slim

ENV SRC_DIR=/app \
    APP_USER=backend-user \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GUNICORN_PROCESSES=4 \
    GUNICORN_CONNECTIONS=8 \
    GUNICORN_LOGLEVEL='error'\
    POETRY_VIRTUALENVS_IN_PROJECT=true\
    PATH="/app/.venv/bin:$PATH"

# Переменные окружения, подтягиваемые из Docker Compose
ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN} \
    WEATHER_API_URL=${WEATHER_API_URL} \
    YANDEX_API_WEATHER_KEY=${YANDEX_API_WEATHER_KEY}

RUN apt-get update && \
    apt-get install -y dos2unix && \
    apt-get install -y gcc libpq-dev

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml /app/

RUN poetry install --no-interaction --no-ansi --no-root

COPY . /app/

COPY bot/ /app/bot/


ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
ENV WEATHER_API_URL=${WEATHER_API_URL}
ENV YANDEX_API_WEATHER_KEY=${YANDEX_API_WEATHER_KEY}


ENTRYPOINT ["bash", "-c", "\
    poetry run python manage.py makemigrations && \
    poetry run python manage.py migrate && \
    poetry run python manage.py collectstatic --noinput && \
    poetry run python manage.py add_user && \
    poetry run python manage.py add_city && \
    poetry run wait-for-it db:5432 --timeout=10 && \
    poetry run celery --app=backend worker -l INFO & \
    poetry run gunicorn --bind 0.0.0.0:8000 --reload backend.wsgi:application & \
    sleep 10 && \
    poetry run python bot/weather_bot.py"]