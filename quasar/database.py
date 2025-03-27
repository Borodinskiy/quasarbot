import sqlite3

class DataBase():
	"""Система хранения базы данных пользователей"""
	def __init__(self, file):
		self.file = file
		self.dbinit(file)

	def dbinit(self, file):
		self.file = file

		database = sqlite3.connect(file)
		cursor = database.cursor()

		# Создание базы данных, если её до этого не было
		cur.execute("CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), stage varchar(50))")
		database.commit()

		cur.close()
		database.close()

	def store_message(message):
		pass
