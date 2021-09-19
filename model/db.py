import sqlite3
import configparser

from model.message import Message


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


class ChannelDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("channel.db")
        __cursor.fetchall()
    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS `channel`(`id` INTEGER PRIMARY KEY AUTOINCREMENT, 
                `text` TEXT NOT NULL,
                `date` TEXT NOT NULL)""")
        self.connection.commit()

    def create_channel(self):
        cursor = self.connection.cursor()
        cursor.execute(""" INSERT INTO 'channel'""")

    def get_channels(self):
        cursor = self.connection.cursor()
        cursor.execute(""" SELECT * FROM 'channel' """)
        return cursor.fetchall()



