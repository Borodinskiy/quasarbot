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
	"Привет, я интеллектуальный бот организации Quasar! Задавай вопросы")

@bot.message_handler(commands = ["flag", "help"])
def cmd_flag(message):
	print(f"someone used bot: {message.from_user.username}")

	bot.send_message(message.chat.id
		, "<b>Hello</b> <em>you</em> are too late for you(<b>self</b>)"
		, parse_mode="html")

@bot.message_handler(commands = ["hello"])
def cmd_hello(message):
	print(f"someone used bot: {message.from_user.username}")

	username = message.from_user.first_name
	if message.from_user.last_name:
		username = username + " " + message.from_user.last_name

	bot.send_message(message.chat.id
		, f"Привет, {username}", reply_to_message_id=message.id)

@bot.message_handler(commands = ["site", "website"])
def cmd_site(message):
	print(f"someone used bot: {message.from_user.username}")

	bot.send_message(message.chat.id
		, f"Наш шедевротрейлер <a href='{website_link}'>quasar.ru</a>"
		, parse_mode="html")

@bot.message_handler(content_types=["photo"])
def received_photo(message):
	markup = types.InlineKeyboardMarkup()

	btn_review = types.InlineKeyboardButton(
		"Оставить отзыв об ответе"
		, callback_data="delete")
	btn_operator = types.InlineKeyboardButton(
		"Пожаловаться на сообщение"
		, url=website_link)

	markup.row(btn_review, btn_operator)
	print(f"someone sended picture: {message.from_user.username}")
	bot.reply_to(message
		, "Нуууууу, не скажу, что плохо. Отправь ещё что-нибудь 👀👀👀."
		, reply_markup=markup)

@bot.message_handler(content_types=["sticker"])
def received_sticker(message):
	print(f"someone sended a sticker: {message.from_user.username}")
	bot.reply_to(message, "👀")

# Этот хендлер должен быть всегда в конце,
# иначе он будет захватывать все последующие
@bot.message_handler()
def chat(message):
	print(f"someone used bot: {message.from_user.username}")

	username = message.from_user.first_name
	if message.from_user.last_name:
		username = username + " " + message.from_user.last_name

	match message.text.lower():
		case "ты крутой":
			bot.reply_to(message
				, f"{username}, ты тоже"
				, reply_to_message_id=message.id
			)
		case "myid":
			bot.send_message(message.chat.id
				, f"Your id is {message.from_user.id}"
			)
		case "whoami":
			bot.send_message(message.chat.id
				, f"Your is {message.from_user.username}"
			)
		case default:
			bot.reply_to(message
				, "Приношу наиумоляюще грубочайшие извинения, но что вы имеете в виду??????")

# Финальные шаги

if __name__ == "__main__":
	bot.polling(none_stop = True)