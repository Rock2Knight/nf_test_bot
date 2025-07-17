import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
#from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler

#from db_handler.db_class import PostgresHandler
from config import settings

#pg_db = PostgresHandler(config('PG_LINK'))
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
admins = [int(admin_id) for admin_id in settings.get_admins().split(',')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=settings.get_token(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())