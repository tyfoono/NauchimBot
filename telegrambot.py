import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


bot = Bot(token="5222944621:AAHVj3rwmMIgdMHgoHZo4YOzO3si1kG-hDU")
dp = Dispatcher(bot)

# Создание клавиатуры с многоразовым показом, кнопки расположены в столбик
button_hi = KeyboardButton('Привет! 👋')
button_it = KeyboardButton('Forum! 🌷')
button_test = KeyboardButton('/test')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).row(
    button_hi, button_it, button_test)


# Создание клавиатуры с модноразовым показом, кнопки в строку
button_z1 = KeyboardButton('Задание1 👋')
button_z2 = KeyboardButton('Задание2 🌷')
button_bye = KeyboardButton('Пока 👣')
greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb1.add(button_z1, button_z2, button_bye)

# Создание инлайн-клавиатуры с многоразовым показом, кнопки в столбик
button_il1 = InlineKeyboardButton('Бот 👋', callback_data='il1')
button_il2 = InlineKeyboardButton('Умница 🌷', callback_data='il2')
button_il3 = InlineKeyboardButton('Красавчик', callback_data='il3')
il_kb = InlineKeyboardMarkup(row_width=3)
il_kb.add(button_il1, button_il2, button_il3)


@dp.callback_query_handler(text="il1")
async def inline1(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, "Да, это я!")


@dp.callback_query_handler(text="il2")
async def inline1(call: types.CallbackQuery):
    print(call)
    await bot.send_message(call.message.chat.id, "Ещё я вышивать умею!")


@dp.callback_query_handler(text="il3")
async def inline1(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, "Ой, ты тоже ничего)")


@dp.message_handler(commands=['norm'])
async def process_hi1_command(message: types.Message):
    await message.reply("Нормальная клавиатура", reply_markup=greet_kb)


@dp.message_handler(text='Кто я')
async def process_life(message: types.Message):
    print(message)
    await bot.send_message(message.from_user.id, "Ты замечательный человек!")


@dp.message_handler(text='Кто ты')
async def process_life(message: types.Message):
    await bot.send_message(message.from_user.id, "Алло...", reply_markup=il_kb)


@dp.message_handler(commands=['test'])
async def process_hi1_command(message: types.Message):
    await message.reply("Очень важное сообщение", reply_markup=greet_kb1)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nЯ твой первый бот для Forum!")
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
           id INTEGER, name TEXT, rate INTEGER, mess TEXT
           )""")
    connect.commit()
    user_id = message.chat.id
    user_name = message.chat.username
    cursor.execute(f'SELECT id FROM login_id WHERE id = {user_id}')
    data = cursor.fetchone()

    print(data)
    print(user_id, user_name)
    if data is None:
        cursor.execute("INSERT INTO login_id VALUES(?,?,?);",
                       (user_id, user_name, 0))
        connect.commit()
    else:
        print("Данные существуют")


@dp.message_handler(commands=['deleteme'])
async def process_help_command(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    user_id = message.chat.id
    cursor.execute(f'DELETE FROM login_id WHERE id = {user_id}')
    connect.commit()


@dp.message_handler(text='IT-Fest! 🌷')
async def process_help_command(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    user_id = message.chat.id
    cursor.execute(f'SELECT rate FROM login_id WHERE id = {user_id}')
    r1 = cursor.fetchone()
    print(r1)
    cursor.execute(f'UPDATE login_id SET rate= {r1[0]+1} WHERE id = {user_id}')
    connect.commit()


@dp.message_handler()
async def echo_message(msg: types.Message):
    if msg.text == "Привет! 👋":
        await bot.send_message(msg.from_user.id, "Молодец нажал кнопку.Что будешь делать дальше?")
    elif msg.text == "Пока! 👋":
        await bot.send_photo(msg.from_user.id, "https://www.sunhome.ru/i/cards/97/virtualnaya-otkritka-s-nadpisyu-poka.orig.png")
    elif msg.text == "Хочешь тестик?":
        await bot.send_message(msg.from_user.id, "https://testometrika.com/personality-and-temper/you-have-high-self-esteem/")
    elif msg.text == "Хочешь песню? 👋":
        await bot.send_message(msg.from_user.id, "https://hitmo.online/songs/top-today/start/96")
    elif msg.text == "Снег? 👋":
        await bot.send_message(msg.from_user.id, "https://s1.1zoom.ru/big0/540/Seasons_Winter_Forests_463761.jpg")
    elif msg.text == "Солнце? 👋":
        await bot.send_message(msg.from_user.id, "https://im0-tub-ru.yandex.net/i?id=f499a011a9a264d74b28af69f3f51f05-l&ref=rim&n=13&w=1080&h=720")
    else:
        await bot.send_message(msg.from_user.id, "Нипонял")


executor.start_polling(dp)
