import random

from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import filters, FSMContext

import func
from config import register
from created_bot import dp, bot

from db_function import Database
db = Database('find_team_lite.db')


# ************************************* найти тиммейта **********************************
@dp.message_handler(filters.Text('Найти тиммейта'))
async def find_team(message: Message):
    users_id = await func.get_users_id(message.from_user.id)

    try:
        number_user_id = random.randint(1, len(users_id))

        user_id_team = users_id[number_user_id - 1]
        mess = await func.gen_mess_by_find_team(user_id_team)
        photo_id = await db.get_photo_id(user_id_team)

        button_1 = InlineKeyboardButton('❤️', callback_data=f'like@{user_id_team}@{int(number_user_id + 1)}')
        button_2 = InlineKeyboardButton('Написать', callback_data=f'write@{user_id_team}')
        button_3 = InlineKeyboardButton('➡️', callback_data=f'next@{int(number_user_id + 1)}')
        markup = InlineKeyboardMarkup().add(button_1, button_3).add(button_2)

        await bot.send_photo(message.from_user.id, photo_id, caption=mess, reply_markup=markup)

    except Exception as e:
        button = KeyboardButton('Меню')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
        await bot.send_message(message.from_user.id, 'Пока мы не нашли ни одного подходящего тиммейта, '
                                                     'загляни позже😥', reply_markup=markup)


# **************************************** лайк *********************************************
@dp.callback_query_handler(lambda call: call.data.startswith('like'))
async def like(call: CallbackQuery, state: FSMContext):
    user_id_team = call.data.split('@')[1]
    number_user = call.data.split('@')[2]

    users_id = await func.get_users_id(call.from_user.id)

    if call.from_user.username is not None:
        username = '@' + call.from_user.username
    else:
        username = call.from_user.first_name

    await bot.send_message(user_id_team, f'❤️ Вы понравились {username}')
    print(number_user, len(users_id))

    if int(number_user) >= len(users_id):
        number_user = 0

    user_id_team = users_id[int(number_user)]
    mess = await func.gen_mess_by_find_team(user_id_team)
    photo_id = await db.get_photo_id(user_id_team)

    button_1 = InlineKeyboardButton('❤️', callback_data=f'like@{user_id_team}@{int(number_user) + 1}')
    button_2 = InlineKeyboardButton('Написать', callback_data=f'write@{user_id_team}')
    button_3 = InlineKeyboardButton('➡️', callback_data=f'next@{int(number_user) + 1}')
    markup = InlineKeyboardMarkup().add(button_1, button_3).add(button_2)

    await bot.send_photo(call.from_user.id, photo_id, caption=mess, reply_markup=markup)
    await bot.delete_message(call.from_user.id, message_id=call.message.message_id)


# **************************************** следующий *********************************************
@dp.callback_query_handler(lambda call: call.data.startswith('next'))
async def next_step(call: CallbackQuery, state: FSMContext):
    number_user = int(call.data.split('@')[1])
    users_id = await func.get_users_id(call.from_user.id)

    if int(number_user) >= len(users_id):
        number_user = 0

    user_id_team = users_id[number_user]
    mess = await func.gen_mess_by_find_team(user_id_team)
    photo_id = await db.get_photo_id(user_id_team)

    button_1 = InlineKeyboardButton('❤️', callback_data=f'like@{user_id_team}@{int(number_user + 1)}')
    button_2 = InlineKeyboardButton('Написать', callback_data=f'write@{user_id_team}')
    button_3 = InlineKeyboardButton('➡️', callback_data=f'next@{int(number_user + 1)}')
    markup = InlineKeyboardMarkup().add(button_1, button_3).add(button_2)

    await bot.send_photo(call.from_user.id, photo_id, caption=mess, reply_markup=markup)
    await bot.delete_message(call.from_user.id, message_id=call.message.message_id)


# **************************************** написать *********************************************
@dp.callback_query_handler(lambda call: call.data.startswith('write'))
async def write(call: CallbackQuery, state: FSMContext):
    user_id_team = call.data.split('@')[1]
    await state.update_data(user_id_team=user_id_team)

    mess = 'Введите текст сообщения⤵'

    await bot.send_message(call.from_user.id, mess)
    await bot.delete_message(call.from_user.id, message_id=call.message.message_id)
    await register.find_team_send_mess.set()


# ********************************** получение текста сообщения | отправка **********************************
@dp.message_handler(state=register.find_team_send_mess)
async def find_team_send_mess(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id_team = data.get('user_id_team')

    if message.from_user.username is not None:
        username = '@' + message.from_user.username
    else:
        username = message.from_user.first_name

    mess = f'📩 Пользователь {username} отправил тебе новое сообщение\n\n' \
           f'"{message.text}"'

    button = InlineKeyboardButton('Ответить', callback_data=f'write@{message.from_user.id}')
    markup = InlineKeyboardMarkup().add(button)
    await bot.send_message(user_id_team, mess, reply_markup=markup)

    await bot.send_message(message.from_user.id, 'Сообщение отправлено🥰')
    await state.finish()


# ********************************** исключения **********************************
@dp.message_handler(state=register.find_team_send_mess)
async def find_team_send_mess_text(message: Message, state: FSMContext):
    if message.text == 'Найти тиммейта':
        users_id = await func.get_users_id(message.from_user.id)

        try:
            number_user_id = random.randint(1, len(users_id))

            user_id_team = users_id[number_user_id - 1]
            mess = await func.gen_mess_by_find_team(user_id_team)
            photo_id = await db.get_photo_id(user_id_team)

            button_1 = InlineKeyboardButton('❤️', callback_data=f'like@{user_id_team}@{int(number_user_id + 1)}')
            button_2 = InlineKeyboardButton('Написать', callback_data=f'write@{user_id_team}')
            button_3 = InlineKeyboardButton('➡️', callback_data=f'next@{int(number_user_id + 1)}')
            markup = InlineKeyboardMarkup().add(button_1, button_3).add(button_2)

            await bot.send_photo(message.from_user.id, photo_id, caption=mess, reply_markup=markup)

        except Exception as e:
            button = KeyboardButton('Меню')
            markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
            await bot.send_message(message.from_user.id, 'Пока мы не нашли ни одного подходящего тиммейта, '
                                                         'загляни позже😥', reply_markup=markup)

    else:
        if not await db.exists_user_id(message.from_user.id):
            button = KeyboardButton('Создать аккаунт')
            markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
        else:
            button_1 = KeyboardButton('Найти тиммейта')
            button_2 = KeyboardButton('Изменить анкету')
            markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)

        await bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!\n'
                                                     f'Приветственное сообщение⤵', reply_markup=markup)





