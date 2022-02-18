from keyboard import greet_key
from aiogram import Dispatcher
from create_bot import dp


# @dp.message_handler(commands=['start'])
async def process_hi_command(message):
    await message.answer_sticker(r'CAACAgQAAxkBAAEDy5Fh-x-svmcxY5AZKtmbD1ey64QiwAACiAADLOlYDEVV-cLQgV_2IwQ')
    await message.reply('<img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot" />' , reply_markup=greet_key)

def register_handlers_settings(dp: Dispatcher):
    dp.register_message_handler(process_hi_command, text = ['Отмена', '/start'])
    # dp.register_message_handler(echo)