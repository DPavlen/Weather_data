import asyncio
import datetime
import logging
import os
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
import requests
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# WEATHER_API_URL = os.getenv("WEATHER_API_URL")
WEATHER_API_URL = "http://localhost:8000/api/weather_city/"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Узнать погоду")]
], resize_keyboard=True)


@dp.message(Command("start"))
async def start_command(message: Message):
    """Приветственное сообщение при старте бота."""

    logger.info(f"Получена команда от юзера {message.from_user.username}")
    await message.reply(
        "Привет! Нажми 'Узнать погоду' и отправь название города, "
        "чтобы узнать погоду.",
        reply_markup=keyboard)


@dp.message(lambda message: message.text == "Узнать погоду")
async def ask_city(message: Message):
    """Запрос на ввод города после нажатия кнопки."""

    logger.info(f"Пользователь {message.from_user.username} нажимает 'Узнать погоду'")
    await message.reply("Введите название города:")


@dp.message()
async def get_weather(message: Message):
    """Обработчик,получения города и отправки запрос на DRF API."""

    city_name = message.text.title()
    logger.info(f"Пользователь {message.from_user.username}"
                f" запрошенная погода для города: {city_name}")
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")

    try:
        response = requests.get(f"{WEATHER_API_URL}?city={city_name}")
        response.raise_for_status()
        if response.status_code == 200:
            weather_data = response.json()
            weather_text = (
                f"Сегодня {current_date}\n"
                f"Погода в {city_name}:\n"
                f"Температура: {weather_data['temp']}°C\n"
                f"Атмосферное давление: {weather_data['pressure_mm']} мм рт. ст.\n"
                f"Скорость ветра: {weather_data['wind_speed']} м/с\n"
                f"Влажность: {weather_data['humidity']}%"
            )
            await message.reply(weather_text)
        elif response.status_code == 404:
            await message.reply("Город не найден. Пожалуйста, попробуйте снова.")
        else:
            await message.reply("Ошибка при получении данных о погоде. "
                                "Повторите попытку позже.")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.reply("Произошла ошибка при обращении к сервису погоды.")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())