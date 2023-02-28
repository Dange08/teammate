from aiogram.types import Message, ReplyKeyboardRemove,  ContentType
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import filters, FSMContext

import func
from config import register
from created_bot import dp, bot

from db_function import Database
db = Database('find_team_lite.db')

agree_change = ['Принять', 'Изменить анкету']


# ************************************* создать аккаунт **********************************
@dp.message_handler(filters.Text('Создать аккаунт'))
async def create_account(message: Message):
    button_1, button_2 = KeyboardButton('Принять'), KeyboardButton('Меню')
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)
    await bot.send_message(message.from_user.id, '❗️ Предупреждение о мошенниках:\n\n'
                                                 'Никому не передавайте свои личные данные '
                                                 '(пароли от аккаунтов и прочее)', reply_markup=markup)


# ************************************* принять **********************************
@dp.message_handler(filters.Text(agree_change))
async def agree(message: Message):
    await bot.send_message(message.from_user.id, 'Как тебя зовут?⤵', reply_markup=ReplyKeyboardRemove())
    await register.create_account_name.set()


# ********************************** получение имени **********************************
@dp.message_handler(state=register.create_account_name)
async def create_account_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    button_1, button_2 = KeyboardButton('ПК'), KeyboardButton('Консоль')
    button_3 = KeyboardButton('Мобильный гейминг')
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1, button_2).add(button_3)
    await bot.send_message(message.from_user.id, 'На какой платформе ты играешь?', reply_markup=markup)
    await register.create_account_platform.set()


# ********************************** получение платформы **********************************
@dp.message_handler(state=register.create_account_platform)
async def create_account_platform(message: Message, state: FSMContext):
    await state.update_data(platform=message.text)

    if message.text == 'ПК':
        button_1, button_2 = KeyboardButton('CS:GO'), KeyboardButton('DOTA 2')
        button_3, button_4 = KeyboardButton('Valorant'), KeyboardButton('Minecraft')
        button_5, button_6 = KeyboardButton('PUBG'), KeyboardButton('Call of Duty')
        button_7 = KeyboardButton('Fortnite')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1, button_2).add(button_3, button_4)
        markup.add(button_5, button_6).add(button_7)
    elif message.text == 'Консоль':
        button_1, button_2 = KeyboardButton('Call of Duty'), KeyboardButton('Fortnite')
        button_3 = KeyboardButton('Minecraft')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1, button_2).add(button_3)
    else:
        button_1, button_2 = KeyboardButton('Minecraft'), KeyboardButton('PUBG')
        button_3 = KeyboardButton('Call of Duty')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1, button_2).add(button_3)

    await bot.send_message(message.from_user.id, 'В какой игре ты бы хотел найти тиммейта?', reply_markup=markup)
    await register.create_account_game.set()


# ********************************** получение игры **********************************
@dp.message_handler(state=register.create_account_game)
async def create_account_game(message: Message, state: FSMContext):
    await state.update_data(game=message.text)
    if message.text == 'CS:GO' or message.text == 'DOTA 2' or message.text == 'Valorant':
        await bot.send_message(message.from_user.id, 'Введите свое звание⤵', reply_markup=ReplyKeyboardRemove())
        await register.create_account_rang.set()

    else:
        await bot.send_message(message.from_user.id, f'Укажи количество часов в '
                                                     f'{message.text}⤵', reply_markup=ReplyKeyboardRemove())
        await register.create_account_hours.set()


# ********************************** получение ранга **********************************
@dp.message_handler(state=register.create_account_rang)
async def create_account_rang(message: Message, state: FSMContext):
    await state.update_data(rang=message.text)
    data = await state.get_data()
    game = data.get('game')
    await bot.send_message(message.from_user.id, f'Укажи количество часов в '
                                                 f'{game}⤵', reply_markup=ReplyKeyboardRemove())
    await register.create_account_hours.set()


# ********************************** получение кол-ва часов **********************************
@dp.message_handler(state=register.create_account_hours)
async def create_account_hours(message: Message, state: FSMContext):
    await state.update_data(hours=message.text)
    button_1, button_2 = KeyboardButton('Мужской'), KeyboardButton('Женский')
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1, button_2)
    await bot.send_message(message.from_user.id, 'Отлично!🤩\n\n'
                                                 '📃 Давай наполним твой профиль информацией, чтобы было проще найти '
                                                 'тебе тиммейта\n\n'
                                                 'Укажи свой пол⤵', reply_markup=markup)
    await register.create_account_gender.set()


# ********************************** получение пола **********************************
@dp.message_handler(state=register.create_account_gender)
async def create_account_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await bot.send_message(message.from_user.id, 'Сколько тебе лет?', reply_markup=ReplyKeyboardRemove())
    await register.create_account_age.set()


# ********************************** получение возраста **********************************
@dp.message_handler(state=register.create_account_age)
async def create_account_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        button_1, button_2 = KeyboardButton('Парня'), KeyboardButton('Девушку')
        button_3 = KeyboardButton('Без разницы')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1, button_2).add(button_3)
        await bot.send_message(message.from_user.id, 'Кого бы ты хотел найти себе в качестве тиммейта?',
                               reply_markup=markup)
        await register.create_account_find_team.set()

    else:
        await bot.send_message(message.from_user.id, '❗️ Введи возраст целым числом')


# ********************************** получение того, кого хочет найти **********************************
@dp.message_handler(state=register.create_account_find_team)
async def create_account_find_team(message: Message, state: FSMContext):
    await state.update_data(find_team=message.text)
    button = KeyboardButton('Любой возраст')
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    await bot.send_message(message.from_user.id, 'Тиммейт какого возраста тебя интересует?\n'
                                                 'Укажите границы через тире (пример: 15-20)', reply_markup=markup)
    await register.create_account_ege_team.set()


# ********************************** получение возраста, кого хочет найти **********************************
@dp.message_handler(state=register.create_account_ege_team)
async def create_account_ege_team(message: Message, state: FSMContext):
    if message.text == 'Любой возраст' or ('-' in message.text and len(message.text) <= 5 and \
            message.text.split('-')[0].isdigit() and message.text.split('-')[1].isdigit()):
        await state.update_data(age_team=message.text)
        await bot.send_message(message.from_user.id, 'Расскажи о себе что-нибудь⤵', reply_markup=ReplyKeyboardRemove())
        await register.create_account_about.set()

    else:
        await bot.send_message(message.from_user.id, '❗️ Введи возраст в указанном формате (нижняя граница-верхняя '
                                                     'граница, 15-20), без пробелов')


# ********************************** получение информации о себе **********************************
@dp.message_handler(state=register.create_account_about)
async def create_account_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await bot.send_message(message.from_user.id, 'Пришли фотографию на аватар🤩')
    await register.create_account_photo.set()


# ********************************** получение фото **********************************
@dp.message_handler(state=register.create_account_photo, content_types=ContentType.PHOTO)
async def create_account_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)

    data = await state.get_data()
    name = data.get('name')
    game = data.get('game')
    rang = data.get('rang')
    platform = data.get('platform')
    hours = data.get('hours')
    gender = data.get('gender')
    age = data.get('age')
    find_team = data.get('find_team')
    age_team = data.get('age_team')
    about = data.get('about')

    mess = await func.gen_mess_by_control(name, game, rang, platform, hours, gender, age, find_team.lower(),
                                          age_team, about)

    button_1, button_2 = KeyboardButton('Подтвердить'), KeyboardButton('Внести правки')
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)

    try:
        await bot.send_photo(message.from_user.id, photo_id, caption=mess, reply_markup=markup)
    except Exception as e:
        await bot.send_photo(message.from_user.id, photo_id, 'Аватар:')
        await bot.send_message(message.from_user.id, mess, reply_markup=markup)

    await register.create_account_finish.set()


# ********************************** окончание ветки  **********************************
@dp.message_handler(state=register.create_account_finish)
async def create_account_finish(message: Message, state: FSMContext):
    if message.text == 'Подтвердить':
        data = await state.get_data()
        name = data.get('name')
        game = data.get('game')
        rang = data.get('rang')
        platform = data.get('platform')
        hours = data.get('hours')
        gender = data.get('gender')
        age = data.get('age')
        find_team = data.get('find_team')
        age_team = data.get('age_team')
        about = data.get('about')
        photo_id = data.get('photo_id')

        if not await db.exists_user_id(message.from_user.id):
            await db.add_user_id(message.from_user.id)

        await db.add_name(name, message.from_user.id)
        await db.add_game(game, message.from_user.id)
        await db.add_rang(rang, message.from_user.id)
        await db.add_platform(platform, message.from_user.id)
        await db.add_hours(hours, message.from_user.id)
        await db.add_gender(gender, message.from_user.id)
        await db.add_age(age, message.from_user.id)
        await db.add_find_team(find_team, message.from_user.id)
        await db.add_age_team(age_team, message.from_user.id)
        await db.add_about(about, message.from_user.id)
        await db.add_photo_id(photo_id, message.from_user.id)

        mess = '🥳 Данные сохранены!\n\n' \
               '🥳 Поздравляем, теперь ты можешь искать тиммейтов⤵'

        button_1 = KeyboardButton('Найти тиммейта')
        button_2 = KeyboardButton('Изменить анкету')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)
        await bot.send_message(message.from_user.id, mess, reply_markup=markup)
        await state.finish()

    else:
        data = await state.get_data()
        game = data.get('game')
        button_1, button_2 = KeyboardButton('Имя'), KeyboardButton('Пол')
        button_3, button_4 = KeyboardButton('Игра'), KeyboardButton('Ранг')
        button_5 = KeyboardButton('Количество часов')
        button_6, button_7 = KeyboardButton('Платформа'), KeyboardButton('Обо мне')
        button_8, button_9 = KeyboardButton('Ищу тиммейта'), KeyboardButton('Возраст тиммейта')

        if game == 'CS:GO' or game == 'DOTA 2' or game == 'Valorant':
            markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1, button_2).add(button_3, button_6)
            markup.add(button_5).add(button_7, button_8).add(button_9)
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1, button_2).add(button_3, button_4)
            markup.add(button_5).add(button_6, button_7).add(button_8, button_9)
        await bot.send_message(message.from_user.id, 'Выбери раздел, где нужны изменения⤵', reply_markup=markup)
        await register.create_account_change_type.set()


# ********************************** получение места изменений **********************************
@dp.message_handler(state=register.create_account_change_type)
async def create_account_change_type(message: Message, state: FSMContext):
    await state.update_data(change_type=message.text)

    if message.text == 'Имя':
        await bot.send_message(message.from_user.id, 'Напиши корректно имя⤵', reply_markup=ReplyKeyboardRemove())

    elif message.text == 'Пол':
        button_1, button_2 = KeyboardButton('Мужской'), KeyboardButton('Женский')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1, button_2)
        await bot.send_message(message.from_user.id, 'Выбери свой пол корректно⤵', reply_markup=markup)

    elif message.text == 'Игра':
        button_1, button_2 = KeyboardButton('CS:GO'), KeyboardButton('DOTA 2')
        button_3 = KeyboardButton('Minecraft')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1, button_2).add(button_3)
        await bot.send_message(message.from_user.id, 'Выбери игру корректно⤵', reply_markup=markup)

    elif message.text == 'Ранг':
        data = await state.get_data()
        game = data.get('game')
        if game == 'CS:GO':
            await bot.send_message(message.from_user.id, 'Введите свое звание⤵', reply_markup=ReplyKeyboardRemove())
        else:
            await bot.send_message(message.from_user.id, 'Укажи свой ранг⤵', reply_markup=ReplyKeyboardRemove())

    elif message.text == 'Платформа':
        button_1, button_2 = KeyboardButton('ПК'), KeyboardButton('Консоль')
        button_3 = KeyboardButton('Мобильный гейминг')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1, button_2).add(button_3)
        await bot.send_message(message.from_user.id, 'На какой платформе ты играешь?', reply_markup=markup)

    elif message.text == 'Количество часов':
        data = await state.get_data()
        game = data.get('game')
        await bot.send_message(message.from_user.id, f'Какое у тебя количество часов '
                                                     f'в {game}?', reply_markup=ReplyKeyboardRemove())

    elif message.text == 'Обо мне':
        await bot.send_message(message.from_user.id, 'Напиши корректную информацию о себе⤵',
                                                     reply_markup=ReplyKeyboardRemove)

    elif message.text == 'Ищу тиммейта':
        button_1, button_2 = KeyboardButton('Парня'), KeyboardButton('Девушку')
        button_3 = KeyboardButton('Без разницы')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1, button_2).add(button_3)
        await bot.send_message(message.from_user.id, 'Кого бы ты хотел себе найти в качесте тиммейта?',
                               reply_markup=markup)

    elif message.text == 'Возраст тиммейта':
        button = KeyboardButton('Любой возраст')
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
        await bot.send_message(message.from_user.id, 'Тиммейт какого возраста тебя интересует?\n'
                                                     'Укажите границы через тире (пример: 15-20)', reply_markup=markup)
    await register.create_account_change_text.set()


# ********************************** получение текста изменений **********************************
@dp.message_handler(state=register.create_account_change_text)
async def create_account_change_text(message: Message, state: FSMContext):
    data = await state.get_data()
    change_type = data.get('change_type')

    name = data.get('name')
    game = data.get('game')
    rang = data.get('rang')
    platform = data.get('platform')
    hours = data.get('hours')
    gender = data.get('gender')
    age = data.get('age')
    find_team = data.get('find_team')
    age_team = data.get('age_team')
    about = data.get('about')
    photo_id = data.get('photo_id')

    if change_type == 'Имя':
        name = message.text
        await state.update_data(name=name)

    elif change_type == 'Пол':
        gender = message.text
        await state.update_data(gender=gender)

    elif change_type == 'Игра':
        game = message.text
        await state.update_data(game=game)

    elif change_type == 'Ранг':
        rang = message.text
        await state.update_data(rang=rang)

    elif change_type == 'Платформа':
        platform = message.text
        await state.update_data(platform=platform)

    elif change_type == 'Количество часов':
        hours = message.text
        await state.update_data(hours=hours)

    elif change_type == 'Ищу тиммейта':
        find_team = message.text
        await state.update_data(find_team=find_team)

    elif change_type == 'Обо мне':
        about = message.text
        await state.update_data(about=about)

    elif change_type == 'Возраст тиммейта':
        age_team = message.text
        await state.update_data(age_team=age_team)

    mess = await func.gen_mess_by_control(name, game, rang, platform, hours, gender, age, find_team.lower(), age_team, about)

    button_1, button_2 = KeyboardButton('Подтвердить'), KeyboardButton('Внести правки')
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2)

    try:
        await bot.send_photo(message.from_user.id, photo_id, caption=mess, reply_markup=markup)
    except Exception as e:
        await bot.send_photo(message.from_user.id, photo_id, 'Аватар:')
        await bot.send_message(message.from_user.id, mess, reply_markup=markup)

    await register.create_account_finish.set()











