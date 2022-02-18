from config import admin_id
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import keyboard
from create_bot import bot, dp

async def send_admin(dp):
    await bot.send_message(chat_id = admin_id, text = "Bot was started")

from handlers import settings, create

settings.register_handlers_settings(dp)
create.register_handlers_create(dp)


executor.start_polling(dp, on_startup=send_admin, skip_updates=True)
