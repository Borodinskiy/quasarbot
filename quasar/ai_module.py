import lmstudio as lms

model = lms.llm("llama-3.2-1b-instruct")

# Неважно как не важно где
def get_ai_response(user_message):
	try:
		return model.respond(user_message)
	except Exception as e:
		return "Извините, я пока не могу ответить на этот вопрос."

print(model.respond("What a alex? KYM"))