from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
import time

storage = MemoryStorage()

bot = Bot(token='5940031430:AAG5Majt5BSkmtpOyYulDu_Av_PzXYspa8E')
dp = Dispatcher(bot, storage=storage)

class FSMadmin(StatesGroup):
    photo = State()
    text = State()
    username = State()
    
history = '-1001714438941'
chat_id = '-1001858702984'
my_id = '1871864817'

button_main = KeyboardButton('Тапсырманы жүктеу 📥')
button_info = KeyboardButton('Ақпарат 📜')
keyboard_Main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_main, button_info)
button_main_yes = KeyboardButton('🖼 бар')
button_main_no = KeyboardButton('🖼 жоқ')
inline_photo_yes = InlineKeyboardButton(text = 'Бар', callback_data='🖼 бар')
inline_photo_no = InlineKeyboardButton(text ='Жоқ', callback_data='🖼 жоқ')
inkeyboard_yes_no = InlineKeyboardMarkup(row_width=2).add(inline_photo_yes, inline_photo_no)
button_cancel = KeyboardButton('Бас тарту ↩️')
keyboard_yes_no_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_main_yes, button_main_no).add(button_cancel)
button_publish = KeyboardButton('Жариялау 📤')
keyboard_publish_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_publish, button_cancel)
keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_cancel)


@dp.message_handler(commands='start', state=None)
async def start(message: types.Message):
    await message.answer('Сәлеметсіз бе!?\n📌Бот арқылы арнаға өз тапсырмаңызды жүктей аласыз.', reply_markup=keyboard_Main)
    await bot.send_message(history, text = f'@{message.from_user.username}')
    
@dp.message_handler(Text(equals='Тапсырманы жүктеу 📥', ignore_case=True), state=None)
async def mains(message: types.Message):
    await message.reply('Тапсыманың суреті бар ма???', reply_markup=inkeyboard_yes_no)
    
@dp.message_handler(Text(equals='Ақпарат 📜', ignore_case=True), state=None)
async def info(message: types.Message):
    await message.answer('Нұсқаулық (Тапсырманы жүктеу 📥 - батырмасы):\nТапсыманың суреті 🖼 - есеп, тест, бақылау немесе орындалуы керек тапсырманың суреті!\nСипаттама - Қысқаша түсіндірме(нестеу керек? қай тапсырма? қашанға дейін?)')


@dp.message_handler(state="*", commands='Бас тарту ↩️')
@dp.message_handler(Text(equals='Бас тарту ↩️', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Сіз тапсырма жүктеуден бас тартыңыз❗️❗️❗️', reply_markup=keyboard_Main, )


@dp.callback_query_handler(text='🖼 бар', state=None)
async def photo_yes(callback: types.CallbackQuery):
    await FSMadmin.photo.set()
    await callback.message.answer('Тапсыманың суреті 🖼:', reply_markup=keyboard_cancel)
    time.sleep(0.5)
    await callback.message.delete()

@dp.callback_query_handler(text='🖼 жоқ', state=None)
async def photo_no(callback: types.CallbackQuery):
    await FSMadmin.text.set()
    await callback.message.answer('Сипаттама 🖊:', reply_markup=keyboard_cancel)
    time.sleep(0.5)
    await callback.message.delete()
    
# @dp.message_handler(Text(equals='🖼 бар', ignore_case=True), state=None)
# async def cancel_handler(message: types.Message):
#     await FSMadmin.photo.set()
#     await message.reply('Тапсыманың суреті 🖼:', reply_markup=keyboard_cancel)
    
# @dp.message_handler(Text(equals='🖼 жоқ', ignore_case=True), state=None)
# async def cancel_handler(message: types.Message):
#     await FSMadmin.text.set()
#     await message.reply('Сипаттама 🖊:', reply_markup=keyboard_cancel)
    

@dp.message_handler(content_types=['photo'], state=FSMadmin.photo)
async def wait_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await bot.send_photo(history, data['photo'])
    await FSMadmin.next()
    await message.reply('Сипаттама 🖊:', reply_markup=keyboard_cancel)
    
@dp.message_handler(Text(equals='Жариялау 📤', ignore_case=True), state=FSMadmin)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            await bot.send_photo(chat_id, data['photo'], f"Сипаттама: {data['text']}\nТелеграм: @{data['username']}")
            await message.answer('Жарияланды!', reply_markup=keyboard_Main)
        except:
            await bot.send_message(chat_id, f"Сипаттама: {data['text']}\nТелеграм: @{data['username']}")
            await message.answer('Жарияланды!', reply_markup=keyboard_Main)
    await state.finish()
    
@dp.message_handler(state=FSMadmin.text)
async def load_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        data['username'] = message.from_user.username
        
    async with state.proxy() as data:
        try:
            await bot.send_photo(message.from_user.id, data['photo'], f"Сипаттама: {data['text']}", reply_markup=keyboard_publish_cancel)
            # await bot.send_photo(chat_id, data['photo'], f"Сипаттама: {data['text']}\nТелеграм: @{data['username']}")
        except:
            await bot.send_message(message.from_user.id, f"Сипаттама: {data['text']}", reply_markup=keyboard_publish_cancel)
            # await bot.send_message(chat_id, f"Нет фото\nСипаттама: {data['text']}\nТелеграм: @{data['username']}")
    # await state.finish()    
    

def main():
    executor.start_polling(dp, skip_updates=True)
    
if __name__ == '__main__':
    
    main()
