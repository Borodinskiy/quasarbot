from telebot import TeleBot, types
import re
from ai_module import get_ai_response

# Ссылка на наш сайт (такого нет) и не будет
WEBSITE_LINK = "https://www.youtube.com/watch?v=XfELJU1mRMg"

TOKENFILE = "token.txt"
DBFILE = "database.db"

WARNING_STRING = "\n❗️❗️❗️Внимание❗️❗️❗️\nНе пишите никаких личных данных (номер телефона, пароли, и прочее) - мошенники не дремлют"

# Инициализация бота и чтение токена из файла
try:
	with open(TOKENFILE) as token:
		bot_token = token.read().strip()  # Убираем лишние пробелы или переносы строк
		bot = TeleBot(bot_token)
except FileNotFoundError:
	print(f"Error when trying to open bot token from \"{TOKENFILE}\"")
	exit()

# TODO: ну какбэ... Реализовать это
try:
	database = None  # Пока заглушка для базы данных
	# database = DataBase(DBFILE)  # Раскомментируйте, когда реализуете класс DataBase
except FileNotFoundError:
	print(f"Error when reading database file from \"{DBFILE}\"")
	exit()


def delete_message_with_personal_data(message):
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

	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton("Да, отправить вопрос", callback_data="confirm_send"))
	markup.add(types.InlineKeyboardButton("Нет, задать вопрос заново", callback_data="restart_question"))

	if found_data:
		warning_message = (
			"⚠️ Похоже, вы ввели персональные данные. Вы уверены, что хотите отправить этот вопрос? "
			"Они могут попасть не в те руки.\nВыберите вариант ответа ниже"
		)
		bot.send_message(message.chat.id, warning_message, reply_markup=markup)

		# Удаляем исходное сообщение с персональными данными
		bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

		# Логируем найденные данные (для администратора или отладки)
		# print("Найдены следующие персональные данные:")
		# for data in found_data:
		#     print(data)
		# Были найдены ПДн
		return True
	# Не найдены ПДн
	return False

# TODO: Стиль - это вид промпта, который надо использовать
def handle_ai_response(message, style = "default"):
	# Если в сообщении не найдены ПДн
	if not delete_message_with_personal_data(message):
		bot.reply_to(message, get_ai_response(message, style))

# Основные декораторы

@bot.message_handler(commands=["start"])
def cmd_start(message):
	print(f"Someone used bot: {message.from_user.username}")
	bot.send_message(message.chat.id, "Привет, я интеллектуальный бот! Задавайте вопросы")
	vopros(message)


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
	if delete_message_with_personal_data(message):
		return

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
			bot.send_message(message.chat.id, f"Напишите свой вопрос {WARNING_STRING}")
			# При получении следующего сообщения от пользователя вызовется уже данная функция
			# и ей передастся аргумент message и style (это реализовать потом)
			bot.register_next_step_handler(message, handle_ai_response, "rncb")

		case "СберБанк":
			bot.send_message(message.chat.id, f"Напишите вопрос {WARNING_STRING}")
			bot.register_next_step_handler(message, handle_ai_response, "sberbank")

		case "Банк АБ Россия":
			bot.send_message(message.chat.id, f"Напишите вопрос {WARNING_STRING}")
			bot.register_next_step_handler(message, handle_ai_response, "ABRussia")

		case "Другой банк":
			bot.send_message(message.chat.id, f"Напишите свой банк, а потом вопрос {WARNING_STRING}")
			bot.register_next_step_handler(message, handle_ai_response, "Russian_bank")

		case "Задать вопрос про Госуслуги":
			bot.send_message(
				message.chat.id,
				f"Хорошо, {username}, что вас интересует? {WARNING_STRING}"
			)

		case "Задать иной вопрос":
			bot.send_message(message.chat.id, f"Хорошо, {username}, что вас интересует? {WARNING_STRING}")

		case "Назад":
			bot.send_message(message.chat.id, "↓↓↓↓", reply_markup=vopros(message))

		case _:
			bot.reply_to(message, "Сейчас отвечу на ваш вопрос")
			bot.send_message(message.chat.id, get_ai_response(message))


# Финальные шаги
if __name__ == "__main__":
	print("aboba")
	bot.polling(none_stop=True)