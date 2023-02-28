from dataclasses import dataclass

from aiogram.dispatcher.filters.state import StatesGroup, State


@dataclass
class Config:
    token: str = '6179334650:AAHdj3uCQVHwQbgn0ZRzsbLIPy9wRWEqkDI'


class register(StatesGroup):
    create_account_name = State()
    create_account_game = State()
    create_account_rang = State()
    create_account_platform = State()
    create_account_hours = State()
    create_account_gender = State()
    create_account_age = State()
    create_account_find_team = State()
    create_account_ege_team = State()
    create_account_about = State()
    create_account_photo = State()
    create_account_finish = State()
    create_account_change_type = State()
    create_account_change_text = State()

    find_team_send_mess = State()
