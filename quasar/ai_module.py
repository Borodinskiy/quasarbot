import lmstudio as lms

model = lms.llm("chatgptdataset_gguf__1instruction_vsgoemotion")

# Неважно как не важно где
def get_ai_response(user_message):
	try:
		return model.respond(user_message)
	except Exception as e:
		return "Извините, я пока не могу ответить на этот вопрос."

