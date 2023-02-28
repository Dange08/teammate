from aiogram import executor
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import filters

from created_bot import bot

from menu.find_team import dp

from db_function import Database
db = Database('find_team_lite.db')


# ************************************************ start **********************************************************
@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    if not await db.exists_user_id(message.from_user.id):
        button = KeyboardButton('Создать аккаунт')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    else:
        button_1 = KeyboardButton('Найти тиммейта')
        button_2 = KeyboardButton('Изменить анкету')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!\n\n'
                                                 f'🙋‍♂️ Добро пожаловать в бот "Teammate"\n\n'
                                                 f'👩‍❤️‍👨 Здесь ты сможешь найти себе друга для совместной игры и '
                                                 f'не только!\n\n'
                                                 f'Уважайте друг друга и приятной игры GLFH)', reply_markup=markup)


# ************************************* меню **********************************
@dp.message_handler(filters.Text('Меню'))
async def menu(message: Message):
    if not await db.exists_user_id(message.from_user.id):
        mess = 'Необходимо создать аккаунт⤵'
        button = KeyboardButton('Создать аккаунт')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    else:
        mess = 'Нажимай, чтобы найти тиммейта⤵'
        button_1 = KeyboardButton('Найти тиммейта')
        button_2 = KeyboardButton('Изменить анкету')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)

    await bot.send_message(message.from_user.id, mess, reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp)
