from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

eventsLinks = {
    'TechnoCom':'vk.com/technocom2022',
    'IT-fest_2022':'vk.com/itfest2022',
    'IASF2022':'vk.com/aerospaceproject'
}

bot = Bot(token='5123538287:AAH7uCEmaKXEYXQ9zspgziNEcb4AKIxKFjI')
dp = Dispatcher(bot)

back_button = types.InlineKeyboardButton(text='Назад', callback_data='start')
back_kb = types.InlineKeyboardMarkup().add(back_button)

buttonLinks = types.KeyboardButton('Контакты 🤙')
startKb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
startKb.add(buttonLinks)

eventsButton = types.

#обработка сообщений

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    text = f'Привет, {first_name}!👋\n'
    await bot.send_message(chat_id, text, reply_markup=startKb)

@dp.message_handler(text='Контакты 🤙', commands=['contacts'])
async def contacts(message: types.Message):
    chat_id = message.chat.id
    text = 'Привет! Если у вас возникли какие-либо вопросы, то вот нашиконтакты:\n Группа ВКонтакте Научим.online https://vk.com/nauchim.online\n Сайт с мероприятиями https://www.научим.online'
    await bot.send_message(chat_id, text, reply_markup=back_kb)

@dp.message_handler(text='Список мероприятий 💻', commands=['list'])
async def events(message: types.Message):
    chat_id = message.chat.id
    text = ''
    await bot.send_message(chat_id, text)

#обработка событий

@dp.callback_query_handler(text='start')
async def back_to_start(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    first_name = call.message.chat.first_name
    text = f'Привет, {first_name}!👋\n'
    await bot.send_message(chat_id, text, reply_markup=startKb)

executor.start_polling(dp)