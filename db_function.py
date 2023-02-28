import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

# ************************************************ USERS ***************************************
    # добавление user_id
    async def add_user_id(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT OR IGNORE INTO `users` (`user_id`) VALUES (?)", (user_id,))

    # проверка наличия user_id
    async def exists_user_id(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    # добавление имени
    async def add_name(self, name, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `name` = ? WHERE `user_id` = ?", (name, user_id))

    # получение имени
    async def get_name(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `name` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                name = row[0]
            return name

    # добавление игры
    async def add_game(self, game, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `game` = ? WHERE `user_id` = ?", (game, user_id))

    # получение игры
    async def get_game(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `game` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                game = row[0]
            return game

    # добавление ранга
    async def add_rang(self, rang, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `rang` = ? WHERE `user_id` = ?", (rang, user_id))

    # получение ранга
    async def get_rang(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `rang` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                rang = row[0]
            return rang

    # добавление платформы
    async def add_platform(self, platform, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `platform` = ? WHERE `user_id` = ?", (platform, user_id))

    # получение платформы
    async def get_platform(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `platform` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                platform = row[0]
            return platform

    # добавление кол-ва часов
    async def add_hours(self, hours, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `hours` = ? WHERE `user_id` = ?", (hours, user_id))

    # получение кол-ва часов
    async def get_hours(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `hours` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                hours = row[0]
            return hours

    # добавление пола
    async def add_gender(self, gender, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `gender` = ? WHERE `user_id` = ?", (gender, user_id))

    # получение пола
    async def get_gender(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `gender` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                gender = row[0]
            return gender

    # добавление возраста
    async def add_age(self, age, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `age` = ? WHERE `user_id` = ?", (age, user_id))

    # получение возраста
    async def get_age(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `age` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                age = row[0]
            return age

    # добавление пола того, кого ищешь
    async def add_find_team(self, find_team, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `find_team` = ? WHERE `user_id` = ?", (find_team, user_id))

    # получение пола того, кого ищешь
    async def get_find_team(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `find_team` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                find_team = row[0]
            return find_team

    # добавление возраста того, кого ищешь
    async def add_age_team(self, age_team, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `age_team` = ? WHERE `user_id` = ?", (age_team, user_id))

    # получение возраста того, кого ищешь
    async def get_age_team(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `age_team` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                age_team = row[0]
            return age_team

    # добавление информации о себе
    async def add_about(self, about, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `about` = ? WHERE `user_id` = ?", (about, user_id))

    # получение информации о себе
    async def get_about(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `about` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                about = row[0]
            return about

    # добавление id фотографии
    async def add_photo_id(self, photo_id, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `photo_id` = ? WHERE `user_id` = ?", (photo_id, user_id))

    # получение id фотографии
    async def get_photo_id(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `photo_id` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                photo_id = row[0]
            return photo_id

    # получение всех user_id по полу и игре (возраст любой)
    async def get_all_user_id(self, gender, game):
        with self.connection:
            gender = '%' + gender + '%'
            result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `gender` LIKE ? AND "
                                         "`game` = ?", (gender, game,)).fetchall()
            result_new = []
            for line in result:
                result_new.append(line[0])
            return result_new

    # получение всех user_id по полу, игре и возрасту
    async def get_all_user_id_with_age(self, gender, game, age_start, age_end):
        with self.connection:
            gender = '%' + gender + '%'
            result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `gender` LIKE ? AND "
                                         "`game` = ?", (gender, game,)).fetchall()
            result_new = []

            for line in result:
                age_ = self.cursor.execute("SELECT `age` FROM `users` WHERE `user_id` = ?", (line[0],)).fetchall()
                for row in age_:
                    age = row[0]

                if age_start <= int(age) <= age_end:
                    result_new.append(line[0])

            return result_new
