import sqlite3

class DataBase():
	"""Система хранения базы данных пользователей"""
	def __init__(self, file):
		self.database = ""

		self.dbinit(file)

	def dbinit(self, file):
		self.database = sqlite3.connect(file)

	def store_message(message):
		pass
