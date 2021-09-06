import sqlite3
import configparser

from message import Message


class ChatDatabase:
    def __init__(self):
        self.cfg_parser = configparser.ConfigParser()
        self.connection = sqlite3.connect("chat.db")

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS `message`(`id` INTEGER PRIMARY KEY AUTOINCREMENT, 
        `text` TEXT NOT NULL,
        `date` TEXT NOT NULL)""")
        self.connection.commit()

    def add(self, message: Message):
        pass



