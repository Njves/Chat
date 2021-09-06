import json
import os
import socket as sock
import threading
from configparser import ConfigParser
from message import Message, MessageSchema


# Библиотека для реализации клиента для сервера
# Нужна реализация слушателя
from protocol import ProtocolSchema, Protocol


class Client:
    CONFIG = 'server_config.ini'

    def __init__(self, listener):
        # Проверяем конфиг
        self.check_config()

        self.listener = listener

        # Инициализируем сокет
        self.socket = sock.socket()
        self.socket.connect(('localhost', 9090))

    def check_config(self):
        # Если конфига нет отрубаем клиента
        if not os.path.isfile(self.CONFIG):
            raise FileExistsError("Конфиг клиента не найден")

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

        except ConnectionResetError as e:
            print("До свидания")

    def get_message_from_server(self):

        while True:
            print("receive")
            # Пришел json объекта Message
            data = self.socket.recv(4096).decode('utf-8')


            protocol_schema = ProtocolSchema()
            protocol = protocol_schema.loads(data)

            # Парсим json

            # Это костыль ебаный с начала пытаемся спарсить список, если получилось отдаем список, если нет все закрвыаемся

            for i in protocol.content:
                message = Message(i['text'], i['sender'])
                self.send_listener_message(message)



    def send_listener_message(self, message):
        if self.listener is not None:
            # Отдаем объект месседж
            self.listener.on_message(message)
