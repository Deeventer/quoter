# БИБЛИОТЕКА ИМПОРТОВ
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()



# ЭКЗЕМПЛЯРЫ

BOT_TOKEN = os.getenv('BOT_TOKEN')


bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=MemoryStorage())