from create_bot import bot, dp
# from balance import all_numbers, all_the_number
from keyboard import greet_key, brcs_key
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from config import pswrds
from database import sqlitedb
from barcoder import decoder

class FSMbarcodes(StatesGroup):
    that = State()
    back = State()

    

# @dp.message_handler(text=["Штрих-коды"], state = None)
async def cmd_start(message: types.Message):
    await FSMbarcodes.that.set()

    # Проверка, есть ли у пользователя номера или нет
    all_numbers = await sqlitedb.sql_find_all_numbers(str(message.from_user.id))

    if len(all_numbers) == 0:
        await bot.send_message(chat_id=message.from_user.id, text='У тебя нет номеров ', reply_markup=brcs_key)
        return
    else:
        string_out = 'Выбери номер:\n'
        for t in range(len(all_numbers)):
            string_out += f"{t}. <b>{str(all_numbers[t][0])}</b>\n"
        print(string_out)

        await message.reply(text=string_out, reply_markup=brcs_key)
    

    


# async def password(message: types.Message, state:FSMContext):
#     await FSMbarcodes.password.set()
#     if message.text in pswrds:
        
#         await FSMbarcodes.that.set()
#         await message.answer_sticker(r'CAACAgUAAxkBAAEDy49h-x6PrB5qE7KQEuEXoU08aX7V6gAC8gIAAq2uOFebuWyag2LaBiME')
#         # await message.reply(text = 'Ок, пароль верный')
#         await bot.send_message(chat_id = message.from_user.id, text = "Для какого номера нужен штрих код?\n" + all_numbers(), reply_markup=brcs_key)
#     else:
#         # await FSMbarcodes.that.set()
#         await message.answer_sticker(r'CAACAgQAAxkBAAEDy4th-x3IXA7Byx6OtruGW-yd3LWYrAACOwADLOlYDPigZCTAOhyBIwQ')
#         # await message.reply("Пароль не верный")


# @dp.message_handler(content_types = ['text'], state = FSMbarcodes.that)
async def find_some(message: types.Message, state: FSMContext):
    print('message: ', message['text'])

    if message.text.replace(" ", "").isdigit() and len(message.text.split()) < 10:
        all_indexs = map(int, message.text.split())
    else:
        await bot.send_message(message.from_user.id, text='Неверный номер!')
        return

    media = types.MediaGroup()

    # Поиск номеров по дб с этим пользователем
    all_numbers = await sqlitedb.sql_find_all_numbers(str(message.from_user.id))

    arr_barcs = []
    for index_num in all_indexs:
        try:
            x = all_numbers[index_num]
        except:
            await bot.send_message(message.from_user.id, text='Неверный номер')
            return
        # print(x, index_num)
        barc = await sqlitedb.sql_find_barcode(x)
        barc = barc[0][0]
        arr_barcs.append(barc)

        path = decoder(barc, barc)
        media.attach_photo(types.InputFile(path), barc)
    await bot.send_media_group(chat_id = message.from_user.id, media=media)
    print()

    print(arr_barcs)

    # status = all_the_number(message.text, len(files))
    
    # if len(message.text.split()) > 10:

    #     await message.reply(text = "Воу, Ошибка, напиши правильно)))")
    #     await message.delete()
    #     return

    # if ' ' in message.text and message.text.replace(' ', '').isdigit():
    #     all_indexs = message.text.split(" ")
    # elif message.text.isdigit():
    #     all_indexs = message.text.split(" ")

    # media = types.MediaGroup()
    # for i in all_indexs:
    #     # if i not in files
    #     path = 'barcoder/'+(files[int(i)]).split(".")[0]+'.gif'
    #     media.attach_photo(types.InputFile(path), 'Превосходная фотография')
    # await bot.send_media_group(chat_id = message.from_user.id, media=media)
    # await FSMbarcodes.next()
    #await bot.send_message(chat_id=message.from_user.id, text=all_barcs)
           

# @dp.message_handler(state='*', commands=['Отмена'])
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(chat_id = message.from_user.id, text = 'Ok', reply_markup=greet_key)



def register_handlers_barcodes(dp: Dispatcher):
    dp.register_message_handler(back, state='*', commands=['Отмена', 'back'])
    dp.register_message_handler(back, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(cmd_start, text=["Штрих-код"], state = None)
    dp.register_message_handler(find_some, state = FSMbarcodes.that)

    

