from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


button_cancel = KeyboardButton('Отмена')

brcs_key = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)

button_create = KeyboardButton('Создать штрих-код')

greet_key = ReplyKeyboardMarkup(resize_keyboard=True).row(button_create)

