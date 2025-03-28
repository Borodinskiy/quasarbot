import lmstudio as lms

# Промты, используемые для различных ситуаций

PROMPT_DEFAULT = """
###Answering Rules###

Следуйте строгому порядку:
Ответ на русском языке.
Назначьте себе роль реального эксперта с конкретной престижной наградой.
Отвечайте пошагово, используя конкретные детали и глубокие знания (шаг 1-й, шаг 2-й и так далее).
Ответ критически важен, излагайте его естественно, без "галлюцинаций".
Используйте структуру ##Answering example## для первого сообщения.
Помни, что пользователь ожидает увидеть ответ для мобильных версий приложений
"""

PROMPT_RNCB = """
Пожалуйста, ответьте на мой вопрос о российском банке "РНКБ"

И теперь мое сообщение вам:

"""
PROMPT_sberbank = """
Пожалуйста, ответьте на мой вопрос о российском банке "Сбер банк"

И теперь мое сообщение вам:

"""
PROMPT_ABRussia = """
Пожалуйста, ответьте на мой вопрос о российском банке "Акционный банк Россия"

И теперь мое сообщение вам:

"""

PROMPT_Russian_bank = """
Пожалуйста, ответьте на мой вопрос о российском банке
Ты должен отвечать как оно должно быть по-идее

И теперь мое сообщение вам:

"""

model = lms.llm("chatgptdataset_gguf__1instruction_vsgoemotion")

# Неважно как не важно где
def get_ai_response(message, style = "default"):
	prompt = ""
	match style:
		case "rncb": prompt = PROMPT_RNCB
		case "sberbank": prompt = PROMPT_sberbank
		case "ABRussia": prompt = PROMPT_ABRussia
		case "Russian_bank": prompt = PROMPT_Russian_bank
		case _: prompt: PROMPT_DEFAULT

	# В завершение дописываем вопрос пользователя
	prompt = prompt + message.text.strip()
	try:
		return model.respond(prompt)
		#return "AI BLAND ANSEWR: aboba"
	except Exception as e:
		return "Извините, я пока не могу ответить на этот вопрос."
