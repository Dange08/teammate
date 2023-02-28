from aiogram import Dispatcher, Bot
from config import Config
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=Config.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot,  storage=MemoryStorage())