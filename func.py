from db_function import Database
db = Database('find_team_lite.db')


async def gen_mess_by_control(name, game, rang, platform, hours, gender, age, find_team, age_team, about):
    mess = 'Проверь корректность введенных данных:\n\n' \
           f'✔️ Имя: {name}\n' \
           f'✔️ Игра: {game}\n' \
           f'✔️ Ранг: {rang}\n' \
           f'✔️ Платформа: {platform}\n' \
           f'✔️ Кол-во часов: {hours}\n' \
           f'✔️ Пол: {gender}\n' \
           f'✔️ Возраст: {age}\n' \
           f'✔️ Я ищу: {find_team.lower()}\n' \
           f'✔️ Возраст тиммейта: {age_team}\n' \
           f'✔️ Обо мне:\n"{about}"\n\n' \
           f'Если все верно, подтверди это по кнопке ниже, в противном случае внеси правки⤵'
    return mess


async def gen_mess_by_find_team(user_id_team):
    name = await db.get_name(user_id_team)
    game = await db.get_game(user_id_team)
    rang = await db.get_rang(user_id_team)
    platform = await db.get_platform(user_id_team)
    hours = await db.get_hours(user_id_team)
    gender = await db.get_gender(user_id_team)
    age = await db.get_age(user_id_team)
    about = await db.get_about(user_id_team)

    mess = f'✔️ {name}\n' \
              f'✔️ Играет в {game}\n' \
              f'✔️ Ранг: {rang}\n' \
              f'✔️ Платформа: {platform}\n' \
              f'✔️ Кол-во часов: {hours}\n' \
              f'✔️ Пол: {gender}\n' \
              f'✔️ Возраст: {age}\n' \
              f'✔️ О себе: "{about}"'
    return mess


async def get_users_id(user_id):
    gender = await db.get_find_team(user_id)

    if gender == 'Девушку':
        gender = 'Женский'
    elif gender == 'Парня':
        gender = 'Мужской'
    else:
        gender = 'й'

    age = await db.get_age_team(user_id)
    game = await db.get_game(user_id)

    if age == 'Любой возраст':
        users_id = await db.get_all_user_id(gender, game)
        users_id = users_id

    else:
        age = age.split('-')
        age_start = int(age[0])
        age_end = int(age[1])
        users_id = await db.get_all_user_id_with_age(gender, game, age_start, age_end)

    try:
        users_id.remove(str(user_id))
    except Exception as e:
        pass

    print(users_id)
    return users_id

