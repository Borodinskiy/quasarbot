from telebot import TeleBot, types

# Ссылка на наш сайт (такого нет)
website_link = "https://www.youtube.com/watch?v=XfELJU1mRMg"

# Инициализация бота и чтение токена из файла
bot = ""
with open("token.txt") as token:
	bot = TeleBot(token.read())

# Основные декораторы

@bot.message_handler(commands = ["start"])
def start(msg):
	print(f"someone used bot: {msg.from_user.username}")

	bot.send_message(msg.chat.id,
	"Привет, я интеллектуальный бот организации Quasar! Задавай вопросы")

@bot.message_handler(commands = ["flag", "help"])
def flag(msg):
	print(f"someone used bot: {msg.from_user.username}")

	bot.send_message(msg.chat.id
		, "<b>Hello</b> <em>you</em> are too late for you(<b>self</b>)"
		, parse_mode="html")

@bot.message_handler(commands = ["hello"])
def hello(msg):
	print(f"someone used bot: {msg.from_user.username}")

	username = msg.from_user.first_name
	if msg.from_user.last_name:
		username = username + " " + msg.from_user.last_name

	bot.send_message(msg.chat.id
		, f"Привет, {username}", reply_to_message_id=msg.id)

@bot.message_handler(commands = ["site", "website"])
def site(msg):
	print(f"someone used bot: {msg.from_user.username}")


	bot.send_message(msg.chat.id
		, f"Наш шедевротрейлер <a href='{website_link}'>quasar.ru</a>"
		, parse_mode="html")

@bot.message_handler(content_types=["photo"])
def photo(msg):
	markup = types.InlineKeyboardMarkup()

	btn_review = types.InlineKeyboardButton(
		"Оставить отзыв об ответе"
		, callback_data="delete")
	btn_operator = types.InlineKeyboardButton(
		"Пожаловаться на сообщение"
		, url=website_link)

	markup.row(btn_review, btn_operator)
	print(f"someone sended picture: {msg.from_user.username}")
	bot.reply_to(msg
		, "Нуууууу, не скажу, что плохо. Отправь ещё что-нибудь 👀👀👀."
		, reply_markup=markup)

@bot.message_handler(content_types=["sticker"])
def photo(msg):
	print(f"someone sended a sticker: {msg.from_user.username}")
	bot.reply_to(msg, "👀")

# Этот хендлер должен быть всегда в конце,
# иначе он будет захватывать все последующие
@bot.message_handler()
def info(msg):
	print(f"someone used bot: {msg.from_user.username}")

	username = msg.from_user.first_name
	if msg.from_user.last_name:
		username = username + " " + msg.from_user.last_name

	match msg.text.lower():
		case "ты крутой":
			bot.reply_to(msg
				, f"{username}, ты тоже"
				, reply_to_message_id=msg.id
			)
		case "myid":
			bot.send_message(msg.chat.id
				, f"Your id is {msg.from_user.id}"
			)
		case "whoami":
			bot.send_message(msg.chat.id
				, f"Your is {msg.from_user.username}"
			)
		case default:
			bot.reply_to(msg
				, "Приношу наиумоляюще грубочайшие извинения, но что вы имеете в виду??????")

# Финальные шаги

bot.polling(none_stop = True)