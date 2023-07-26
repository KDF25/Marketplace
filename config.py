from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config_telegram import *

storage = RedisStorage2()
# storage = MemoryStorage()
scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
scheduler.start()

bot = Bot(token=str(token), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)



