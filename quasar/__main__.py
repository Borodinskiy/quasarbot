from telebot import TeleBot, types
import re

# Ссылка на наш сайт (такого нет) и не будет
website_link = "https://www.youtube.com/watch?v=XfELJU1mRMg"

tokenfile = "token.txt"
dbfile = "database.db"

warning_string = "\n❗️❗️❗️Внимание❗️❗️❗️\nНе пишите никаких личных данных (номер телефона, пароли, и прочее) - мошенники не дремлют"

# Инициализация бота и чтение токена из файла
try:
    with open(tokenfile) as token:
        bot_token = token.read().strip()  # Убираем лишние пробелы или переносы строк
        bot = TeleBot(bot_token)
except FileNotFoundError:
    print(f"Error when trying to open bot token from \"{tokenfile}\"")
    exit()

# TODO: ну какбэ... Реализовать это
try:
    database = None  # Пока заглушка для базы данных
    # database = DataBase(dbfile)  # Раскомментируйте, когда реализуете класс DataBase
except FileNotFoundError:
    print(f"Error when reading database file from \"{dbfile}\"")
    exit()


def delete_message_with_personal_data(message):
    """
    Проверяет сообщение на наличие персональных данных и удаляет его, если данные найдены.
    """
    patterns = {
        "emails": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
        "phones": r'(\+?\d{1,3}[-.\s]?)?(\(?\d{1,4}\)?[-.\s]?)?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
        "passwords": r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}',
        "ips": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        "dates": r'\b(?:\d{1,2}[./-]\d{1,2}[./-]\d{2,4})\b'
    }

    found_data = []
    for category, pattern in patterns.items():
        matches = re.findall(pattern, message.text)
        if matches:
            found_data.append(f"{category.capitalize()}: {matches}")

    if found_data:
        warning_message = ( "⚠️ Похоже, вы ввели персональные данные. Вы уверены, что хотите отправить этот вопрос? "
"Они могут попасть не в те руки. Вы уверенны, что хотите отправить это сообщение?")
        bot.send_message(message.chat.id, warning_message)

        # Удаляем сообщение с персональными данными
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

        # Логируем найденные данные (для администратора или отладки)
        print("Найдены следующие персональные данные:")
        for data in found_data:
            print(data)


# Основные декораторы

@bot.message_handler(commands=["start"])
def cmd_start(message):
    print(f"Someone used bot: {message.from_user.username}")
    bot.send_message(message.chat.id, "Привет, я интеллектуальный бот! Задавайте вопросы")


def vopros(message):
    markup = types.ReplyKeyboardMarkup()
    battom1 = types.KeyboardButton("Задать вопрос про банк")
    markup.row(battom1)
    battom2 = types.KeyboardButton("Задать вопрос про Госуслуги")
    markup.row(battom2)
    battom3 = types.KeyboardButton("Задать иной вопрос")
    markup.row(battom3)

    bot.send_message(message.chat.id, "Выберите опцию снизу", reply_markup=markup)


# Этот хендлер должен быть всегда в конце,
# иначе он будет захватывать все последующие
@bot.message_handler(func=lambda message: True)
def chat(message):
    print(f"Someone used bot: {message.from_user.username}")

    username = message.from_user.first_name
    if message.from_user.last_name:
        username = username + " " + message.from_user.last_name

    # Проверяем сообщение на наличие персональных данных
    delete_message_with_personal_data(message)

    markup = types.ReplyKeyboardMarkup()
    match message.text:
        case "Задать вопрос про банк":
            battom1 = types.KeyboardButton("Банк РНКБ")
            markup.row(battom1)
            battom3 = types.KeyboardButton("СберБанк")
            battom2 = types.KeyboardButton("Банк АБ Россия")
            markup.row(battom2, battom3)
            battom4 = types.KeyboardButton("Другой банк")
            markup.row(battom4)
            battom_esc = types.KeyboardButton("Назад")
            markup.row(battom_esc)
            bot.reply_to(message, f"Выберите банк", reply_to_message_id=message.id, reply_markup=markup)

        case "Банк РНКБ":
            bot.send_message(message.chat.id, f"Напишите свой вопрос {warning_string}")

        case "СберБанк":
            bot.send_message(message.chat.id, f"Напишите вопрос {warning_string}")

        case "Банк АБ Россия":
            bot.send_message(message.chat.id, f"Напишите вопрос {warning_string}")

        case "Другой банк":
            bot.send_message(message.chat.id, f"Напишите свой банк, а потом вопрос {warning_string}")

        case "Задать вопрос про Госуслуги":
            bot.send_message(
                message.chat.id,
                f"Хорошо, {username}, что вас интересует? {warning_string}"
            )

        case "Задать иной вопрос":
            bot.send_message(message.chat.id, f"Хорошо, {username}, что вас интересует? {warning_string}")

        case "Назад":
            bot.send_message(message.chat.id, "↓↓↓↓", reply_markup=vopros(message))

        case _:
            bot.reply_to(message, "Сейчас отвечу на ваш вопрос")


# Финальные шаги
if __name__ == "__main__":
    bot.polling(none_stop=True)