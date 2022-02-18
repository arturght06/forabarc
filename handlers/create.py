from create_bot import bot, dp
import barcode
from barcode.writer import ImageWriter
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from keyboard import greet_key, brcs_key


# ean = barcode.get('ean13', barcode_init, writer=ImageWriter())

class FSMcreate(StatesGroup):
    that = State()

async def cmd_start(message: types.Message):
    await FSMcreate.that.set()
    await bot.send_message(chat_id = message.from_user.id, text = "Введи код для генерации" , reply_markup=brcs_key)

async def barcode_gen(message: types.Message, state: FSMContext):
	try:
		ean = barcode.get('ean13', message.text, writer=ImageWriter())
	except:
		await message.reply(text='Возникла ошибка при создании штрих-кода')
		return
	# await bot.send_photo(chat_id=message.chat.id, photo=ean)
	ph = open(ean.save('files/' + str(message.text)), 'rb')
	media = types.MediaGroup()
	media.attach_photo(ph, 'Твой штрих-код ' + message.text)
	await bot.send_media_group(chat_id=message.from_user.id, media=media)


async def back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(chat_id = message.from_user.id, text = 'Ok', reply_markup=greet_key)

def register_handlers_create(dp: Dispatcher):
    dp.register_message_handler(back, state='*', commands=['Отмена', 'back'])
    dp.register_message_handler(back, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(cmd_start, text=["Создать штрих-код"], state = None)
    dp.register_message_handler(barcode_gen, state = FSMcreate.that)

