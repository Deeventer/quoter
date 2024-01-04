# БИБЛИОТЕКА ИМПОРТОВ
from aiogram.dispatcher.filters.state import State, StatesGroup


# КЛАССЫ

class InterQuote(StatesGroup):
    inter = State()
    confirm = State()