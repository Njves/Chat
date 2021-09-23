import os
import socket as sock
import threading
from configparser import ConfigParser
from model.message import Message

# Библиотека для реализации клиента для сервера
# Нужна реализация слушателя
from model.protocol import Protocol, from_json


class Client:
    CONFIG = '../server_config.ini'
    is_connected = False

    def __init__(self, listener):
        # Проверяем конфиг
        self.check_config()

        self.listener = listener

        # Инициализируем сокет
        self.socket = sock.socket()


    def init(self):
        self.connect()

    def connect(self):
        if self.is_connected:
            return
        try:
            self.socket.connect(('localhost', 9090))
        except ConnectionError as e:
            self.listener.on_failed(e)
            self.is_connected = False
            return
        self.listen()
        self.is_connected = True
        self.listener.on_connected()

    def check_config(self):
        # Если конфига нет отрубаем клиента
        if not os.path.isfile(self.CONFIG):
            raise FileExistsError("Конфиг клиента не найден")

    def on_failed(self, error):
        print(f"Неудалось подключиться\n{error}")
        self.listener.on_failed(error)

    # Получить порт из конфига
    def get_port(self):
        cfg_parser = ConfigParser()
        cfg_parser.read(self.CONFIG)
        return int(cfg_parser['server']['port'])

    def send_message(self, protocol: Protocol):
        self.socket.send(bytes(protocol.to_json(), encoding='UTF-8'))

    def listen(self):
        self.t = threading.Thread(target=self.get_message_from_server, args=())
        self.t.start()

    def disconnect(self):
        try:
            self.t.join()
            self.socket.close()
            self.listener.on_disconnect()
        except ConnectionResetError as e:
            print("До свидания")

    def get_message_from_server(self):
        while True:
            # Пришел json объекта Message
            data = self.socket.recv(4096).decode('utf-8')
            # Парсим json
            protocol = from_json(data)
            for i in protocol.content:
                message = Message(i['text'], i['sender'])
                self.send_listener_message(message)

    def send_listener_message(self, message):
        if self.listener is not None:
            # Отдаем объект месседж
            self.listener.on_message(message)
