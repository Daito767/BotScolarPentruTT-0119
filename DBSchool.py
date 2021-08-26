import inspect
import mysql.connector
import datetime
import pytz
import time


def reconnect(func: classmethod):
	def new_func(self, *args, **kwargs):
		if time.time() - self.last_connection_time > self.minutes_passed_for_reconnection:
			self.mydb = mysql.connector.connect(host=self.host, user=self.user, password=self.db_password)
			self.last_connection_time = time.time()
			self.mycursor = self.mydb.cursor()
			self.mycursor.execute(f'USE {self.db_name}')

		func(self, *args, **kwargs)  # Se executa functia originala.

	new_func.__name__ = func.__name__
	sig = inspect.signature(func)
	new_func.__signature__ = sig.replace(parameters=tuple(sig.parameters.values()))
	return new_func


class ConnectToDB:
	def __init__(self, host: str, user: str, password: str, db_name: str, minutes_for_reconnection: int = 5):
		"""
		Creaza o clasa pentru interactiunea cu baza de date.
		"""
		self.host = host
		self.user = user
		self.db_password = password
		self.db_name = db_name
		self.mydb = mysql.connector.connect(host=self.host, user=self.user, password=self.db_password)
		self.last_connection_time = time.time()
		self.mycursor = self.mydb.cursor()
		self.mycursor.execute(f'USE {self.db_name}')
		self.minutes_passed_for_reconnection = minutes_for_reconnection * 60

	@reconnect
	def add_startup_log(self):
		"""
		Salveaza datata si ora rularii bot-ului.
		"""
		dt = datetime.datetime.now(pytz.timezone("Europe/Chisinau"))
		self.mycursor.execute(f'INSERT INTO `StartUpLogs` (`DataSiOra`) VALUES ("{dt.date()} {dt.time()}")')
		self.mydb.commit()
