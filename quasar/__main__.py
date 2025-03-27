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
	"Привет, я интеллектуальный бот! Задавай вопросы")
	markup = types.ReplyKeyboardMarkup()
	battom1 = types.KeyboardButton("Задать вопрос про банк")
	markup.row(battom1)
	battom2 = types.KeyboardButton("Задать вопрос про Госуслуги")
	markup.row(battom2)
	battom3 = types.KeyboardButton("Задать вопрос про Медицинские полисы")
	markup.row(battom3)
	battom4 = types.KeyboardButton("Задать иной вопрос")
	markup.row(battom4)
	bot.send_message(message.chat.id, "Чем могу вам помочь сегодня?", reply_markup=markup)
# @bot.message_handler(commands = ["flag", "help"])
# def cmd_flag(message):
# 	print(f"someone used bot: {message.from_user.username}")
#
# 	bot.send_message(message.chat.id
# 		, "<b>Hello</b> <em>you</em> are too late for you(<b>self</b>)"
# 		, parse_mode="html")

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

	match message.text:
		case "Задать вопрос про банк":
			bot.reply_to(message
				, f"Хорошо, {username}, что вас интересует?"
				, reply_to_message_id=message.id
			)
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
		case default:
			bot.reply_to(message
				, "Приношу наиумоляюще грубочайшие извинения, но что вы имеете в виду??????")

# Финальные шаги

if __name__ == "__main__":
	bot.polling(none_stop = True)