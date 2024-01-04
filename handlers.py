# БИБЛИОТЕКА ИМПОРТОВ
import random

import aiogram
import sqlite3

from config import dp
from functions import *
from states import InterQuote


# /START , РЕГИСТРАЦИЯ

@dp.message_handler(commands=['start'], state='*')
async def start(msg: aiogram.types.Message):

    if await CheckUser.registration(userid=msg.from_user.id):
        await msg.reply('Вы уже зарегистрированы!')

    else:
        db = sqlite3.connect('database.db')
        db.cursor().execute('INSERT INTO users (id, username, full_name) VALUES (?,?,?)',
                            (msg.from_user.id, f'@{msg.from_user.username}', msg.from_user.full_name))
        db.commit()
        db.close()

        await msg.reply('Добро пожаловать!')


# /HELP , ПОМОЩЬ ПО КОМАНДАМ
    
@dp.message_handler(commands=['help', 'commands'], state='*')
async def help(msg: aiogram.types.Message):
    
    if await CheckUser.registration(userid=msg.from_user.id):
        await msg.answer('<b>СПИСОК КОМАНД:</b>\n\n'
                         '- /help : посмотреть команды бота ;\n\n'
                         '- /quote : опубликовать цитату ;\n'
                         '- /quotes : посмотреть случайную цитату .')

    else:
        await msg.reply('Вы не зарегистрированы! Введите /start .')


# /QUOTE , ПУБЛИКАЦИЯ ЦИТАТЫ

@dp.message_handler(commands='quote', state='*')
async def inter_state(msg: aiogram.types.Message):
    
    if await CheckUser.registration(userid=msg.from_user.id):
        await msg.answer('Напишите вашу цитату. Если хотите отменить действие, нажмите на кнопку ниже.',
                         reply_markup=aiogram.types.InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [aiogram.types.InlineKeyboardButton(text='Отмена', callback_data='q:cancel')]
                             ]
                         ))
        await InterQuote.inter.set()
    
    else:
        await msg.reply('Вы не зарегистрированы! Введите /start .')


@dp.message_handler(state=InterQuote.inter)
async def inter_state2(msg: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    
    await state.update_data(quote=msg.text)
    await InterQuote.confirm.set()

    await msg.answer(f'Вы точно хотите опубликовать цитату?\n"{msg.text}"',
                     reply_markup=aiogram.types.InlineKeyboardMarkup(
                         inline_keyboard=[
                             [aiogram.types.InlineKeyboardButton(text='Опубликовать', callback_data='q:confirm'),
                              aiogram.types.InlineKeyboardButton(text='Отмена', callback_data='q:cancel')]
                         ]
                     ))
    

@dp.callback_query_handler(aiogram.filters.Text(startswith='q:'), state='*')
async def confirm_state(query: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    await query.answer()
    category = query.data.split(':')[1]

    if category == 'cancel':
        await query.message.edit_text('Действие отменено!')
        await state.reset_state(with_data=True)

    elif category == 'confirm':
        quote = await state.get_data()
        quote = quote['quote']
        
        db = sqlite3.connect('database.db')
        db.cursor().execute('INSERT INTO quotes (creatorid, quote) VALUES (?,?)',
                            (query.from_user.id, quote))
        db.commit()
        db.close()

        await state.reset_state(with_data=True)
        await query.message.edit_text('Ваша цитата успешно опубликована!')


# /QUOTES , ПРОСМОТР ВСЕХ ЦИТАТ

@dp.message_handler(commands='quotes', state='*')
async def see_quotes(msg: aiogram.types.Message):

    if await CheckUser.registration(userid=msg.from_user.id):
        db = sqlite3.connect('database.db')
        all_quotes = db.cursor().execute('SELECT quote FROM quotes').fetchall()
        quotes = [quote[0] for quote in all_quotes]
        db.close()

        random_quote = random.choice(quotes)
        await msg.answer(random_quote)
    
    else:
        await msg.reply('Вы не зарегистрированы! Введите /start .')