import sys
import vk
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import sqlite3

# подключение базы данных

connect = sqlite3.connect('users.db')
cursor = connect.cursor()

# починка ошибки юникода

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# токены

vk_token = 'token'
chat_id = ''

# инициализация телеграм бота

bot = Bot(token='token')
dp = Dispatcher(bot)

# клавиатура главного меню

buttonList = types.KeyboardButton('Список мероприятий 🌟')
buttonLinks = types.KeyboardButton('Контакты 🤝')
buttonUpdate = types.KeyboardButton('Проверить на наличие новых записей 💬')
buttonHelp = types.KeyboardButton('Путеводитель по боту 🧭')
startKb = types.ReplyKeyboardMarkup(one_time_keyboard=True).row(buttonList).row(buttonLinks).row(buttonUpdate).row(buttonHelp)

# клавиатура мероприятий

linksKb = types.InlineKeyboardMarkup()
linkNeuro = types.InlineKeyboardButton('🧠 «Нейрофест» - Всероссийский фестиваль нейротехнологий', callback_data='Neuro')
linkItFest = types.InlineKeyboardButton('💻 «IT-FEST» - Международный фестиваль информационных технологий', callback_data='ItFest')
linkIASF = types.InlineKeyboardButton('🛰 Международный аэрокосмический фестиваль (IASF)', callback_data='IASF')
linkOKK = types.InlineKeyboardButton('🎉 Фестиваль общекультурных компетенций', callback_data='OKK')
linkIW = types.InlineKeyboardButton('🔬 «Невидимый мир» - Всероссийский конкурс по микробиологии', callback_data='IW')
linkTC = types.InlineKeyboardButton('🌟 «TechnoCom» - Международный конкурс детских инженерных команд', callback_data='TC')
linkVR = types.InlineKeyboardButton('🕶 VR/AR Fest - Международный фестиваль 3D-моделирования и программирования', callback_data='VR')
linkNIR = types.InlineKeyboardButton('📖 Всероссийский конкурс научно-исследовательских работ', callback_data='NIR')
linksKb.row(linkNeuro).row(linkIW)
linksKb.row(linkItFest).row(linkTC)
linksKb.row(linkOKK).row(linkNIR)
linksKb.row(linkIASF).row(linkVR)

# словари для работы с вк

tags = {
    'Neuro':'Нейрофест',
    'ItFest':'ITFest_2022',
    'TechnoCom':'TechnoCom',
    'IASF':'IASF2022',
    'Okk':'ФестивальОКК',
    'IW':'НевидимыйМир',
    'NIR':'КонкурсНИР',
    'VRAR':'VRARFest3D'
}
owners = {
    'Neuro':'-211803420',
    'ItFest':'-210985709',
    'TechnoCom':'-210998761',
    'IASF':'-196557207',
    'Okk':'-211638918',
    'IW':'-200248443',
    'NIR':'-200248443',
    'VRAR':'-200248443'
}
subs = {
    'subNeuro':True,
    'subItFest':False,
    'subTechnoCom':False,
    'subIASF':False,
    'subOkk':False,
    'subIW':False,
    'subNIR':False,
    'subVRAR':False
}
lastId = {
    'Neuro':0,
    'ItFest':0,
    'TechnoCom':0,
    'IASF':0,
    'Okk':0,
    'IW':0,
    'NIR':0,
    'VRAR':0
}
lastPosts = {
    'Neuro':None,
    'ItFest':None,
    'TechnoCom':None,
    'IASF':None,
    'Okk':None,
    'IW':None,
    'NIR':None,
    'VRAR':None
}
first = {
    'Neuro':'🧠 «Нейрофест» - Всероссийский фестиваль нейротехнологий',
    'ItFest':'💻 «IT-FEST» - Международный фестиваль информационных технологий',
    'TechnoCom':'🌟 «TechnoCom» - Международный конкурс детских инженерных команд',
    'IASF':'🛰 Международный аэрокосмический фестиваль (IASF)',
    'Okk':'🎉 Фестиваль общекультурных компетенций',
    'IW':'🔬 «Невидимый мир» - Всероссийский конкурс по микробиологии',
    'NIR':'📖 Всероссийский конкурс научно-исследовательских работ',
    'VRAR':'🕶 VR/AR Fest - Международный фестиваль 3D-моделирования и программирования'
}

############################
# функции для работы с sal #
############################

# инициализация базы данных

def dbExecute(chat_id, first_name, username):
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
           id INTEGER PRIMARY KEY,
           name TEXT, 
           username TEXT
           )""")
    connect.commit()
    cursor.execute(f'SELECT id FROM login_id WHERE id = {chat_id}')
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO login_id VALUES(?,?,?);",
                       (chat_id, first_name, username))
        connect.commit()

#получение имени пользователя

def get_name(chat_id):
    cursor.execute(f'SELECT name FROM login_id WHERE id = {chat_id}')
    line = str(cursor.fetchone())
    for char in '()\',':  
        line = line.replace(char, '')
    return line  


#######################################
# получение последней записи со стены #
#######################################

async def get_post(chat_id,key):
    if chat_id != '':
        session = vk.Session(access_token=vk_token) 
        vk_api = vk.API(session)
        new = False
        owner_id = owners.get(key)
        post = vk_api.wall.get(owner_id=owner_id, v=5.92, count=1, offset=0)['items'][0]
        if post['id'] != lastId.get(key):  
            if tags.get(key) in post['text']:
                text = first.get(key) + '\n\n\n'
                text += post['text']
                lastId[key] = post['id']
                new = True
                await bot.send_message(chat_id, text) 
        return new

#######################
# обработка сообщений #
#######################

# путеводитель

@dp.message_handler(text=['/help', 'Путеводитель по боту 🧭'])
async def help(message: types.Message):
    text = 'Путеводитель по боту 🧭\n\n\n'
    text +=' 🌟 кнопка "Список мероприятий" или команада "/list" - \n'
    text +='    вывод списка мероприятий и информации о них 🌟 \n\n'
    text +=' 🤝 кнопка "Контакты" или команада "/contacts" - \n'
    text +='    вывод контактов организаторов 🤝\n\n'
    text +=' 💬 кнопка "Проверить на наличие новых записей" или команада "/update" - \n'
    text +='    проверка групп в ВКонтакте на наличие записей по тегам и выводит текст последней записи 💬\n\n'
    text +=' 👍 команада "/suball" - \n'
    text +='    подписка на рассылку о всех мероприятиях 👍\n\n'
    text +=' 👎 команада "/unsuball" - \n'
    text +='    отписка от рассылки о всех мероприятиях 👎\n\n'
    text +=' ☹ команада "/bye":\n'
    text +='    удаляет данные о пользователе из базы данных ☹\n\n'
    await bot.send_message(message.chat.id, text)

# обновление данных записей

@dp.message_handler(text=['/update', 'Проверить на наличие новых записей 💬'])
async def update(message: types.Message):
    chat_id = message.chat.id
    for key in list(owners.keys()):
        if subs.get('sub' + key) == True:
            new = await get_post(chat_id, key)
            if new == False:
                await bot.send_message(chat_id, f'{first.get(key)}\nПока ничего нового...')

# начальное сообщение

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    username = message.chat.username
    text = f'Привет, {first_name}!👋\n'
    await bot.send_message(chat_id, text, reply_markup=startKb)
    dbExecute(chat_id, first_name, username)

# удаление из базы данных

@dp.message_handler(commands=['bye'])
async def bye(message: types.Message):
    chat_id = message.chat.id
    first_name = get_name(chat_id)
    await bot.send_message(chat_id, f'Пока, {first_name}, ☹...')
    cursor.execute(f'DELETE FROM login_id WHERE id = {chat_id}')
    connect.commit()

# вывод контактов

@dp.message_handler(text=['/contacts', 'Контакты 🤝'])
async def contacts(message: types.Message):
    chat_id = message.chat.id
    first_name = get_name(chat_id)
    text = f'Если у вас возникли какие-либо вопросы, {first_name} ,то вот наши контакты:\n\n • Группа ВКонтакте Научим.online https://vk.com/nauchim.online\n • Сайт с мероприятиями https://www.научим.online'
    await bot.send_message(chat_id, text)

# вывод списка мероприятий

@dp.message_handler(text=['/list', 'Список мероприятий 🌟'])
async def events(message: types.Message):
    chat_id = message.chat.id
    text = 'Вот список наших мероприятий: '
    await bot.send_message(chat_id, text, reply_markup=linksKb)

# подписка на все мероприятия

@dp.message_handler(commands=['suball'])
async def suball(message: types.Message):
    for key in list(subs.keys()):
        subs[key] = True
    await bot.send_message(message.chat.id, 'Теперь вы подписаны на рассылку о всех мероприятиях! 👍')

# отписка от всех мероприятий

@dp.message_handler(commands=['unsuball'])
async def suball(message: types.Message):
    for key in list(subs.keys()):
        subs[key] = False
    await bot.send_message(message.chat.id, 'Теперь вы отписаны от рассылки о всех мероприятиях! 👎')

#####################
# обработка событий #
#####################

# запросы на подписку

@dp.callback_query_handler(text=list(subs.keys()))
async def sub(call: types.CallbackQuery):
    if subs.get(call.data) == True:
        await bot.send_message(call.message.chat.id, 'Вы уже подписаны на рассылку этого мероприятия!')
    else:
        subs[call.data] = True
        await bot.send_message(call.message.chat.id, 'Теперь вы подписаны на рассылку новостей мероприятия!')

# запросы на получение информации

@dp.callback_query_handler(text=['Neuro', 'ItFest', 'OKK', 'IASF', 'IW', 'TC', 'VR', 'NIR'])
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
            site_url = 'https://www.научим.online/it-fest-2022'
            text += f' • Группа ВКонтакте: {vk_url}\n'
            text += f' • Сайт мероприятия: {site_url}'
            path = 'images/it-fest.jpg'
            data = 'subItFest'
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
            data = 'subOkk'
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
            data = 'subTechnoCom'
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
            data = 'subVRAR'
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

########################
# запуск по расписанию #
########################

#в разработке

executor.start_polling(dp)
