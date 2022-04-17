 #Комманды:
# - /list - вывод списка всех мероприятий
# - /contacts - вывод контактов организаторов +
# - /help - помощь
# - /suball - подписка на все мероприятия
# - /unsuball - отписка от всех мероприятий

import sys
import vk
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import sqlite3

connect = sqlite3.connect('users.db')
cursor = connect.cursor()

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

vk_token = '9dfa07419dfa07419dfa0741cd9d8619c999dfa9dfa0741ffae5478875654c94509d144'
chat_id = ''

bot = Bot(token='5123538287:AAEr4uxOd1VZYCX1-EiPAiab0EO-PwazhCw')
dp = Dispatcher(bot)

buttonList = types.KeyboardButton('Список мероприятий 🌟')
buttonLinks = types.KeyboardButton('Контакты 🤝')
startKb = types.ReplyKeyboardMarkup(one_time_keyboard=True).row(buttonList).row(buttonLinks)

linksKb = types.InlineKeyboardMarkup()
linkNeuro = types.InlineKeyboardButton('🧠 «Нейрофест» - Всероссийский фестиваль нейротехнологий', callback_data='Neuro')
linkItFest = types.InlineKeyboardButton('💻 «IT-FEST» - Международный фестиваль информационных технологий', callback_data='ItFest')
linkIASF = types.InlineKeyboardButton('🛰 Международный аэрокосмический фестиваль (IASF)', callback_data='IASF')
linkOKK = types.InlineKeyboardButton('🎉 Фестиваль общекультурных компетенций', callback_data='OKK')
linkIW = types.InlineKeyboardButton('🔬 «Невидимый мир» - Всероссийский конкурс по микробиологии', callback_data='IW')
linkTC = types.InlineKeyboardButton('🌟 «TechnoCom» - Международный конкурс детских инженерных команд', callback_data='TC')
linkVR = types.InlineKeyboardButton('🕶 VR/AR Fest - Международный фестиваль 3D-моделирования и программирования', callback_data='VR')
linkNIR = types.InlineKeyboardButton('📖 Всероссийский конкурс научно-исследовательских работ', callback_data='NIR')
linksKb.row(linkNeuro, linkIW)
linksKb.row(linkItFest, linkTC)
linksKb.row(linkOKK, linkNIR)
linksKb.row(linkIASF, linkVR)

############################
# функции для работы с sal #
############################

def dbExecute(chat_id, first_name):
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
           id INTEGER PRIMARY KEY,
           name TEXT, 
           Neuro INTEGER,
           ItFest INTEGER,
           Okk INTEGER,
           IASF INTEGER,
           IW INTEGER,
           TechnoCom INTEGER,
           VRAR INTEGER,
           NIR INTEGER
           )""")
    connect.commit()
    cursor.execute(f'SELECT id FROM login_id WHERE id = {chat_id}')
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO login_id VALUES(?,?,?,?,?,?,?,?,?,?);",
                       (first_name, 0, 0, 0, 0, 0, 0, 0, 0))
        connect.commit()

#######################################
# получение последней записи со стены #
#######################################

async def get_posts(chat_id, owner_id):
    session = vk.Session(access_token=vk_token) 
    vk_api = vk.API(session)
    mas = vk_api.wall.get(owner_id=owner_id, v=5.92, count=1, offset=0)
    if "#ITfest_2022" in mas['items'][0]['text']:
        await bot.send_message(chat_id, mas['items'][0]['text'])
    return mas

#######################
# обработка сообщений #
#######################

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    text = f'Привет, {first_name}!👋\n'
    await bot.send_message(chat_id, text, reply_markup=startKb)
    await get_posts(chat_id, '-210985709')
    dbExecute(chat_id, first_name)

@dp.message_handler(commands=['bye'])
async def bye(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    user_id = message.chat.id
    cursor.execute(f'DELETE FROM login_id WHERE id = {user_id}')
    connect.commit()

@dp.message_handler(text=['/contacts', 'Контакты 🤝'])
async def contacts(message: types.Message):
    chat_id = message.chat.id
    text = f'Если у вас возникли какие-либо вопросы, {message.chat.first_name} ,то вот наши контакты:\n\n • Группа ВКонтакте Научим.online https://vk.com/nauchim.online\n • Сайт с мероприятиями https://www.научим.online'
    await bot.send_message(chat_id, text)


@dp.message_handler(text=['/list', 'Список мероприятий 🌟'])
async def events(message: types.Message):
    chat_id = message.chat.id
    text = 'Вот список наших мероприятий: '
    await bot.send_message(chat_id, text, reply_markup=linksKb)

#####################
# обработка событий #
#####################

@dp.callback_query_handler()
async def linksHandler(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    text = 'Ошибка ⚠'
    path = 'images/error.png'
    vk_url = 'https://vk.com/nauchim.online'
    site_url = 'https://www.научим.online/'
    data = 'error'
    match call.data:
        case 'Neuro':
            text = '🧠 «Нейрофест» - Всероссийский фестиваль нейротехнологий\n\n\n'
            text += '✔️ Интересуетесь работой мозга, нейрокомпьютерными интерфейсами, искусственным интеллектом и когнитивными исследованиями?\n\n'
            text +=  'Специально для вас открывается Всероссийский фестиваль нейротехнологий «Нейрофест»! На нём вас ждут научно-популярные лекции экспертов, мастер-классы от партнеров, где участники, даже самые маленькие, познакомятся с основными трендами и достижениями нейронаук и технологий.\n\n\n'
            text += '🧒Возраст участников:\n\n'
            text += ' • 5-17 лет\n\n\n'
            text += '🌐 Ссылки: \n\n'
            vk_url = 'https://vk.com/neurofest2022'
            site_url = 'https://www.научим.online/neuro-fest-2022'
            text += f' • Группа ВКонтакте: {vk_url}\n'
            text += f' • Сайт мероприятия: {site_url}'
            path = 'images/neuro.jpg'
            data = 'subNeuro'
        case 'ItFest':
            text = '💻 «IT-FEST» - Международный фестиваль информационных технологий\n\n\n'
            text += '✔️ Хочешь погрузиться в мир информационных технологий, принять участие в мастер-классах от высококвалифицированных специалистов крупных IT-компаний и уже сейчас начать реализовывать себя как программиста?\n\n'
            text += 'Тогда добро пожаловать на самый масштабный IT фестиваль, где ты получишь уникальную возможность выйти на международную арену и вырасти из Junior-разработчика в Middle в самый короткий срок, а также расширить свой профессиональный круг знакомств.\n\n\n'
            text += '🧒Возраст участников:\n\n'
            text += ' • 7-17 лет\n\n\n'          
            text += '🌐 Ссылки: \n\n'
            vk_url = 'https://vk.com/itfest2022'
            site_url  = 'https://www.научим.online/it-fest-2022'
            text += f' • Группа ВКонтакте: {vk_url}\n'
            text += f' • Сайт мероприятия: {site_url}'
            path = 'images/it-fest.jpg'
            data='subItFest'
        case 'OKK':
            text = '🎉 Фестиваль общекультурных компетенций\n\n\n'
            text += '✔️СЕМЬ тематических мероприятий\n'
            text += '✔️СЕМЬ творческих заданий\n'
            text += '✔️лекции, мастерклассы и ИСТОРИИ УСПЕХА\n'
            text += '✔️челленджи, марафоны, квизы и другие игры\n'
            text += '✔️единый рейтинг для всех участников\n'
            text += '✔️ЛЮБОЙ уровень знаний и РАЗНЫЕ увлечения\n'
            text += '✔️ВОЗМОЖНОСТЬ проявить себя\n\n'
            text += 'Здесь будет интересно школьнику, увлекающемуся IT, юному натуралисту или обучающимся художественной школы. Ты сможешь проявить себя индивидуально и продемонстрировать умение работать в команде.\n\n\n'
            text += '🧒Возраст участников:\n\n'
            text += ' • 5-18 лет\n\n\n'
            text += '🌐 Ссылки: \n\n'
            vk_url = 'https://vk.com/okk_fest'
            site_url  = 'https://www.научим.online/cultural-skills-2022'
            text += f' • Группа ВКонтакте: {vk_url}\n'
            text += f' • Сайт мероприятия: {site_url}'
            path = 'images/okk.jpg'
            data = 'subOKK'
        case 'IASF':
            text = '🛰 Международный аэрокосмический фестиваль (IASF)\n\n\n'
            text += '✔️ Онлайн-площадка, объединяющая всех увлечены космосом и авиацией\n\n'
            text += '✔️ Фестиваль соберет самые яркие мероприятия и ключевые космические события всей страны\n\n'
            text += '✔️ На Фестивале вы познакомитесь с ведущими экспертами отрасли, действующими космонавтами, сможете задать им вопросы и воплотить свои идеи в реальность\n\n\n'
            text += '🧒Возраст участников:\n\n'
            text += ' • 10-17 лет\n\n\n'
            text += '🌐 Ссылки: \n\n'
            vk_url = 'https://vk.com/aerospaceproject'
            site_url = 'https://www.научим.online/aerospace-fest-2022'
            text += f' • Группа ВКонтакте: {vk_url}\n'
            text += f' • Сайт мероприятия: {site_url}'
            path = 'images/aerospace.jpg'
            data = 'subIASF'
        case 'IW':
            text = '🔬 «Невидимый мир» - Всероссийский конкурс по микробиологии\n\n\n'
            text += '✔️ Нравится изучать микроорганизмы?\n\n'
            text += '✔️ Считаешь себя будущим микробиологом?\n\n'
            text += '✔️ Хочешь просто разобраться в этой теме?\n\n'
            text += 'Этот конкурс для тебя!\n\n'
            text += 'Покажи результаты своей научно-исследовательской или проектной работы по микробиологии и смежным с этой областью наук.\n\n\n'
            text += '🧒Возраст участников:\n\n'
            text += ' • 12-18 лет\n\n\n'
            text += '🌐 Ссылки: \n\n'
            site_url = 'https://www.научим.online/microbiology-2022'
            text += f' • Группа ВКонтакте: {vk_url}\n'
            text += f' • Сайт мероприятия: {site_url}'
            path = 'images/iw.jpg'
            data = 'subIW'
        case 'TC':
            text = '🌟 «TechnoCom» - Международный конкурс детских инженерных команд\n\n\n'
            text += '✔️ Мероприятие для всех, кто интересуется техническим творчеством, актуальными тенденциями развития науки и технологии\n\n'
            text += '✔️ Собирайте команду и испытайте свои силы в работе над актуальными и перспективными проектами!\n\n\n'
            text += '🧒Возраст участников:\n\n'
            text += ' • 9-18 лет\n\n\n'
            text += '🌐 Ссылки: \n\n'
            vk_url = 'https://vk.com/technocom2022'
            site_url = 'https://www.научим.online/engineering-command-2022'
            text += f' • Группа ВКонтакте: {vk_url}\n'
            text += f' • Сайт мероприятия: {site_url}'
            path = 'images/tc.jpg'
            data = 'subTC'
        case 'VR':
            text = '🕶 VR/AR Fest - Международный фестиваль 3D-моделирования и программирования\n\n\n'
            text += '✔️ Мероприятие для всех, кто интересуется техническим творчеством, актуальными тенденциями развития науки и технологии\n\n'
            text += '✔️ Собирайте команду и испытайте свои силы в работе над актуальными и перспективными проектами!\n\n\n'
            text += '🧒Возраст участников:\n\n'
            text += ' • 5-18 лет\n\n\n'
            text += '🌐 Ссылки: \n\n'
            site_url = 'https://www.научим.online/vrar-fest-2022'
            text += f' • Группа ВКонтакте: {vk_url}\n'
            text += f' • Сайт мероприятия: {site_url}'
            path = 'images/vrar.png'
            data = 'subVR'
        case 'NIR':
            text = '📖 Всероссийский конкурс научно-исследовательских работ\n\n\n'
            text += '✔️ Творческий конкурс будет интересен начинающим инженерам и изобретателям со стажем\n\n'
            text += '✔️ Напишите научное исследование на одну из ДЕВЯТИ тем!\n\n'
            text += '✔️ Получите путёвку в ВДЦ "Океан" на смену "Юниквант"!\n\n\n'
            text += '🧒Возраст участников:\n\n'
            text += ' • 12-17 лет\n\n\n'
            text += '🌐 Ссылки: \n\n'
            site_url = 'https://www.научим.online/scientific-research-2022'
            text += f' • Группа ВКонтакте: {vk_url}\n'
            text += f' • Сайт мероприятия: {site_url}'
            path = 'images/vrar.png'
            data = 'subNIR'
    keyVkRedirect = types.InlineKeyboardButton('Перейти в группу ВКонтакте!', url=vk_url)
    keySiteRedirect = types.InlineKeyboardButton('Перейти на сайт!', url=site_url)
    keySub = types.InlineKeyboardButton('Подписаться на рассылку!', callback_data=data)
    kbListFunctions = types.InlineKeyboardMarkup().row(keyVkRedirect).row(keySiteRedirect).row(keySub)
    await bot.send_photo(chat_id, open(path, 'rb'), caption=text, reply_markup=kbListFunctions) 



executor.start_polling(dp)
