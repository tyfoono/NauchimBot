#Комманды:
# - /list - вывод списка всех мероприятий
# - /contacts - вывод контактов организаторов +
# - /help - помощь
# - /suball - подписка на все мероприятия
# - /unsuball - отписка от всех мероприятий


from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher


#временно
eventsLinks = {
    'TechnoCom':'technocom2022',
    'ITfest_2022':'itfest2022',
    'IASF2022':'aerospaceproject',
    'ФестивальОКК':'okk_fest',
    'Нейрофест':'neurofest2022',
    'НевдимыйМир':'nauchim.online',
    'КонкурсНИР':'nauchim.online',
    'VRARFest3D':'nauchim.online'
}

bot = Bot(token='5123538287:AAH7uCEmaKXEYXQ9zspgziNEcb4AKIxKFjI')
dp = Dispatcher(bot)

buttonList = types.KeyboardButton('Список мероприятий 💻')
buttonLinks = types.KeyboardButton('Контакты 🤙')
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

#######################
# обработка сообщений #
#######################

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    text = f'Привет, {first_name}!👋\n'
    await bot.send_message(chat_id, text, reply_markup=startKb)

@dp.message_handler(text=['/contacts', 'Контакты 🤙'])
async def contacts(message: types.Message):
    chat_id = message.chat.id
    text = 'Привет! Если у вас возникли какие-либо вопросы, то вот наши контакты:\n Группа ВКонтакте Научим.online https://vk.com/nauchim.online\n Сайт с мероприятиями https://www.научим.online'
    await bot.send_message(chat_id, text)


@dp.message_handler(text=['/list', 'Список мероприятий 💻'])
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
    text = ''
    path = ''
    match call.data:
        case 'Neuro':
            text = '🧠 «Нейрофест» - Всероссийский фестиваль нейротехнологий\n\n\n'
            text += '✔️ Интересуетесь работой мозга, нейрокомпьютерными интерфейсами, искусственным интеллектом и когнитивными исследованиями?\n\n'
            text +=  'Специально для вас открывается Всероссийский фестиваль нейротехнологий «Нейрофест»! На нём вас ждут научно-популярные лекции экспертов, мастер-классы от партнеров, где участники, даже самые маленькие, познакомятся с основными трендами и достижениями нейронаук и технологий.\n\n\n'
            text += '🧒Возраст участников:\n\n'
            text += ' • 5-17 лет\n\n\n'
            text += '🌐 Ссылки: \n\n'
            text += ' • Группа ВКонтакте: https://vk.com/neurofest2022\n'
            text += ' • Сайт мероприятия: https://www.научим.online/neuro-fest-2022'
            path = 'images/neuro.jpg'
        case 'ItFest':
            text = '💻 «IT-FEST» - Международный фестиваль информационных технологий\n\n\n'
            text += '✔️ Хочешь погрузиться в мир информационных технологий, принять участие в мастер-классах от высококвалифицированных специалистов крупных IT-компаний и уже сейчас начать реализовывать себя как программиста?\n\n'
            text += 'Тогда добро пожаловать на самый масштабный IT фестиваль, где ты получишь уникальную возможность выйти на международную арену и вырасти из Junior-разработчика в Middle в самый короткий срок, а также расширить свой профессиональный круг знакомств.\n\n\n'
            text += '🧒Возраст участников:\n\n'
            text += ' • 7-17 лет\n\n\n'
            text += '🌐 Ссылки: \n\n'
            text += ' • Группа ВКонтакте: https://vk.com/itfest2022\n'
            text += ' • Сайт мероприятия: https://www.научим.online/it-fest-2022'
            path = 'images/it-fest.jpg'
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
            text += ' • Группа ВКонтакте: https://vk.com/okk_fest\n'
            text += ' • Сайт мероприятия: https://www.научим.online/cultural-skills-2022'
            path = 'images/okk.jpg'
        case 'IASF':
            text = '🛰 Международный аэрокосмический фестиваль (IASF)\n\n\n'
            text += '✔️ Онлайн-площадка, объединяющая всех увлечены космосом и авиацией\n\n'
            text += '✔️ Фестиваль соберет самые яркие мероприятия и ключевые космические события всей страны\n\n'
            text += '✔️ На Фестивале вы познакомитесь с ведущими экспертами отрасли, действующими космонавтами, сможете задать им вопросы и воплотить свои идеи в реальность\n\n\n'
            text += '🧒Возраст участников:\n\n'
            text += ' • 10-17 лет\n\n\n'
            text += '🌐 Ссылки: \n\n'
            text += ' • Группа ВКонтакте: https://vk.com/aerospaceproject\n'
            text += ' • Сайт мероприятия: https://www.научим.online/aerospace-fest-2022'
            path = 'images/aerospace.jpg'
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
            text += ' • Группа ВКонтакте: https://vk.com/nauchim.online\n'
            text += ' • Сайт мероприятия: https://www.научим.online/microbiology-2022'
            path = 'images/iw.jpg'
        case 'TC':
            text = '🌟 «TechnoCom» - Международный конкурс детских инженерных команд\n\n\n'
            text += '✔️ Мероприятие для всех, кто интересуется техническим творчеством, актуальными тенденциями развития науки и технологии\n\n'
            text += '✔️ Собирайте команду и испытайте свои силы в работе над актуальными и перспективными проектами!\n\n\n'
            text += '🧒Возраст участников:\n\n'
            text += ' • 9-18 лет\n\n\n'
            text += '🌐 Ссылки: \n\n'
            text += ' • Группа ВКонтакте: https://vk.com/technocom2022\n'
            text += ' • Сайт мероприятия: https://www.научим.online/engineering-command-2022'
            path = 'images/tc.jpg'
        case 'VR':
            text = '🕶 VR/AR Fest - Международный фестиваль 3D-моделирования и программирования\n\n\n'
            text += '✔️ Мероприятие для всех, кто интересуется техническим творчеством, актуальными тенденциями развития науки и технологии\n\n'
            text += '✔️ Собирайте команду и испытайте свои силы в работе над актуальными и перспективными проектами!\n\n\n'
            text += '🧒Возраст участников:\n\n'
            text += ' • 5-18 лет\n\n\n'
            text += '🌐 Ссылки: \n\n'
            text += ' • Группа ВКонтакте: https://vk.com/nauchim.online\n'
            text += ' • Сайт мероприятия: https://www.научим.online/vrar-fest-2022'
            path = 'images/vrar.png'
    await bot.send_photo(chat_id, open(path, 'rb'), caption=text) 


executor.start_polling(dp)
