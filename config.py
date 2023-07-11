from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from attrs import define, field


# storage = RedisStorage2()
storage = MemoryStorage()
scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
scheduler.start()

PGUSER = "postgres"
PASSWORD = "karimov"
token = '5504892953:AAH-WUECmS8AUckggr1BhzKnTN5_FEgBoBQ'
ip = 'localhost'

moderation_chat_id = -1001856703028

bot = Bot(token=str(token), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

chat_id_our = -1001767085919


