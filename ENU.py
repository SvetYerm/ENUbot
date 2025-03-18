import telebot
from telebot import types

TOKEN = "7884289213:AAEnkrdVMjEFDaLcTx97eA7s6csoy_lxmpQ"
bot = telebot.TeleBot(TOKEN)

# Состояния для вопросов
ASKING_QUESTIONS, SHOWING_MENU = range(2)

# Вопросы
questions = [
    "1️⃣ Как вас зовут?",
    "2️⃣ Работаете ли в настоящее время и род Вашей деятельности?",
    "3️⃣ Почему Вы выбрали этот ВУЗ для продолжения образования?",
    "4️⃣ Владеете ли Вы иностранным языком на уровне В2 и выше. Если да, то укажите каким?",
    "5️⃣ Хотели ли бы Вы участвовать в программе по академической мобильности?",
]

# Хранение данных пользователей
user_data = {}
user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = []  # Сбрасываем данные
    user_states[chat_id] = ASKING_QUESTIONS  # Устанавливаем состояние
    bot.send_message(chat_id, questions[0])  # Задаем первый вопрос

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == ASKING_QUESTIONS)
def ask_questions(message):
    chat_id = message.chat.id
    user_data[chat_id].append(message.text)  # Сохраняем ответ

    # Определяем, какой вопрос задавать дальше
    if len(user_data[chat_id]) < len(questions):
        bot.send_message(chat_id, questions[len(user_data[chat_id])])
    else:
        user_states[chat_id] = SHOWING_MENU  # Переходим к меню
        show_menu(chat_id)

def show_menu(chat_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📜 Тема магистерской диссертации")
    btn2 = types.KeyboardButton("📩 Выбор учебных дисциплин")
    btn3 = types.KeyboardButton("ℹ️ Образовательные платформы")
    btn4 = types.KeyboardButton("🎓 Полезные советы")
    btn5 = types.KeyboardButton("🔙 Начать заново")
    keyboard.add(btn1, btn2, btn3)
    keyboard.add(btn4, btn5)

    bot.send_message(chat_id, "✅ Спасибо за ответы! Выберите действие:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == SHOWING_MENU)
def handle_menu(message):
    chat_id = message.chat.id
    text = message.text

    if text == "📜 Тема магистерской диссертации":
        bot.send_message(chat_id, '''В течении двух недель необходимо определиться с темой магистерской диссертации, выбрать руководителя и встретиться с ним. 
1. Данная ссылка, где Вы можете ознакомиться с темами магистерских диссертаций прошлых лет - https://hse.enu.kz/ru/page/departments/department-of-pedagogics/topics-of-theses-masters-and-doctoral-theses
2. Найти информацию о педагогах кафедры, изучить их направления и выбрать руководителя диссертации - https://hse.enu.kz/ru/page/departments/department-of-pedagogics/topics-of-theses-masters-and-doctoral-theses
3. Ознакомиться с различными диссертационными работами на сайте библиотеки ЕНУ - https://library.enu.kz/ProtectedView/Book/ViewBook/91192
4. Сделать регистрацию в библиотечной системе по ссылке - https://www.instagram.com/library_enu?igsh=c2xybXprZWl1cWxx
    После ознакомления нужно заполнить ИПМ в электронной версии с опорой на Положение по магистратуре и Образовательные программы - прикреплен ниже
    Далее, нужно распечатать и подписать ИПМ в А3 формате. 📑 Распечатать можно по адерсу: ул. Кажымукана 18 , номер полиграфии: tel:+77786904728
    После всего этого, напишите и опубликуйте минимум 2 статьи за год, список изданий
''')
    
        with open("data.xlsx", "rb") as file:
            bot.send_document(chat_id, file, caption="Список изданий 📄")

        with open("data2.pdf", "rb") as file:
            bot.send_document(chat_id, file, caption="Положение по магистратуре и образовательные программы 📄")

    if text == "📩 Выбор учебных дисциплин":
            bot.send_message(chat_id, '''Выбор учебных дисциплин: 
                Перейдите по ссылке и ознакомьтесь с Образовательной программой - https://hse.enu.kz/ru/page/departments/department-of-pedagogics/education-programme
                Подать заявление заведующему кафедрой о назначении дисциплин, иначе выбор сделает кафедра.
        ''')
    elif text == "ℹ️ Образовательные платформы":
            bot.send_message(chat_id, ''' 1. Закачать и проверить работу МУК, ТИМС, Платонус ЕНУ. Для МУК и ТИМС нужен личный аккаунт, иначе посещаемость не отразится.
2. После просмотра лекции в МУК ЕНУ отмечайте её как выполненную (кнопка «Выполнено»). То же с тестами.''')
    elif text == "🎓 Полезные советы":
            bot.send_message(chat_id, '''1. При болезни подайте заявление с документами в деканат в течение 5 дней, иначе пропуск останется неуважительным в Платонус. 
2. Для свободного пропуска в корпусы ЕНУ необходимо оформить Face-ID. При его отсутвии, обратиться: Аудитория 114 в главном корпусе по улице Сатпаева 2
3. При проблемах обращаться в техподдержку - tel:+77077423297''')
    elif text == "🔙 Начать заново":
            start(message)  # Запускаем снова

bot.polling()
