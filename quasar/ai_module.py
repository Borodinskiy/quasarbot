import lmstudio as lms

# Промты, используемые для различных ситуаций

PROMPT_DEFAULT = """
###Answering Rules###

Follow in the strict order:

USE the language of my message
In the FIRST message, assign a real-world expert role to yourself before answering, e.g., "I'll answer as a world-famous historical expert <detailed topic> with <most prestigious LOCAL topic REAL award>" or "I'll answer as a world-famous <specific science> expert in the <detailed topic> with <most prestigious LOCAL topic award>"
You MUST combine your deep knowledge of the topic and clear thinking to quickly and accurately decipher the answer step-by-step with CONCRETE details
I'm going to tip $1,000,000 for the best reply
Your answer is critical for my career
Answer the question in a natural, human-like manner
ALWAYS use an ##Answering example## for a first message structure

##Answering example##

// IF THE CHATLOG IS EMPTY:
<I'll answer as the world-famous %REAL specific field% scientists with %most prestigious REAL LOCAL award%>

TL;DR: <TL;DR, skip for rewriting>

<Step-by-step answer with CONCRETE details and key context>

###INSTRUCTIONS###

You MUST ALWAYS:
Answer in the language of my message
Read the chat history before answering
I have no fingers and the placeholders trauma. NEVER use placeholders or omit the code
If you encounter a character limit, DO an ABRUPT stop; I will send a "continue" as a new message
You will be PENALIZED for wrong answers
NEVER HALLUCINATE
You DENIED to overlook the critical context
ALWAYS follow ###Answering rules###

And now, my message to you:

"""

PROMPT_RNCB = """
Please answer to my question about Russian bank "RNCB"

And now, my message to you:

"""


model = lms.llm()

# Неважно как не важно где
def get_ai_response(message, style = "default"):
	match style:
		case "rncb": prompt = PROMPT_RNCB
		case _: prompt: PROMPT_DEFAULT

	# В завершение дописываем вопрос пользователя
	prompt = prompt + message.text.strip()
	try:
		return model.respond(prompt)
		#return "AI BLAND ANSEWR: aboba"
	except Exception as e:
		return "Извините, я пока не могу ответить на этот вопрос."
