# import openai
# from config import OPENAI_API_KEY
#
# openai.api_key = OPENAI_API_KEY
# #неважно как не важно где
# def get_ai_response(user_message):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[{"role": "user", "content": user_message}]
#         )
#         return response["choices"][0]["message"]["content"]
#     except Exception as e:
#         return "Извините, я пока не могу ответить на этот вопрос."
