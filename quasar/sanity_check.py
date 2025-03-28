# Модуль для проверки ответов нейросети на адекватность

rus = "йцукенгшщзхъфывапролджэячсмитьбю"

def check_rus(string):
	for c in string:
		# Если найден хотя бы один русский символ
		if rus.find(c) > -1:
			return True

	return False

