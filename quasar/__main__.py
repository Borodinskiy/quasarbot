from telebot import TeleBot, types

from bot import Bot
from database import DataBase

# Ссылка на наш сайт (такого нет) и не будет
website_link = "https://www.youtube.com/watch?v=XfELJU1mRMg"

tokenfile = "token.txt"

dbfile = "database.db"

# Инициализация бота и чтение токена из файла
bot = ""
try:
	with open(tokenfile) as token:
		bot = TeleBot(token.read())
except FileNotFoundError:
	print(f"Error when trying open bot token from \"{tokenfile}\"")
	exit()

# TODO: ну какбэ... Реализовать это
database = ""
try:
	database = DataBase(dbfile)
except FileNotFoundError:
	print(f"Error when reading database file from \"{dbfile}\"")
	exit()

# Основные декораторы

@bot.message_handler(commands = ["start"])
def cmd_start(message):
	print(f"someone used bot: {message.from_user.username}")

	bot.send_message(message.chat.id,
	"Привет, я интеллектуальный бот! Задавайте вопросы")
def vopros(message):
	markup = types.ReplyKeyboardMarkup()
	battom1 = types.KeyboardButton("Задать вопрос про банк")
	markup.row(battom1)
	battom2 = types.KeyboardButton("Задать вопрос про Госуслуги")
	markup.row(battom2)
	battom3 = types.KeyboardButton("Задать вопрос про Медицинские полисы")
	markup.row(battom3)
	battom4 = types.KeyboardButton("Задать иной вопрос")
	markup.row(battom4)
	bot.send_message(message.chat.id, "Выберите опцию снизу", reply_markup=markup)


# Этот хендлер должен быть всегда в конце,
# иначе он будет захватывать все последующие
@bot.message_handler()
def chat(message):
	print(f"someone used bot: {message.from_user.username}")

	username = message.from_user.first_name
	if message.from_user.last_name:
		username = username + " " + message.from_user.last_name
	markup = types.ReplyKeyboardMarkup()
	match message.text:
		case "Задать вопрос про банк":
			battom1 = types.KeyboardButton("Банк РНКБ")
			markup.row(battom1)
			battom3 = types.KeyboardButton("СберБанк")
			battom2 = types.KeyboardButton("Банк АБ Россия")
			markup.row(battom2, battom3)
			battom_esc = types.KeyboardButton("Назад")
			markup.row(battom_esc)
			bot.reply_to(message, f"Задайте вопрос", reply_to_message_id=message.id, reply_markup=markup)
		case "Задать вопрос про Госуслуги":
			bot.send_message(message.chat.id
				, f"Хорошо, {username}, что вас интересует?"
			)
		case "Задать вопрос про Медицинские полисы":
			bot.send_message(message.chat.id
				, f"Хорошо, {username}, что вас интересует?"
			)

		case "Задать иной вопрос":
			bot.send_message(message.chat.id
							 , f"Хорошо, {username}, что вас интересует?"
							 )
		case "Назад":
			bot.send_message(message.chat.id, "↓↓↓↓", reply_markup=vopros(message))
		case default:
			bot.reply_to(message
				, "Приношу извинения, но я не понимаю. Перефразируйте?")

# Финальные шаги

if __name__ == "__main__":
	bot.polling(none_stop = True)