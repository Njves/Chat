import json
import os
import socket as sock
import threading
from configparser import ConfigParser
from message import Message, MessageSchema
from message import from_dict


# Базовая обертка над клиентом
# Нужна реализация слушателя


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

    def send_message(self, message):
        self.socket.send(bytes(message, encoding='UTF-8'))

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
        print("receive")
        while True:
            # Пришел json объекта Message
            data = self.socket.recv(4096).decode('utf-8')
            print(data)
            # Парсим json
            # Это костыль ебаный с начала пытаемся спарсить список, если получилось отдаем список, если нет все закрвыаемся
            raw_json = json.loads(data)
            if isinstance(raw_json, list):
                for i in raw_json:
                    message = from_dict(i['text'])
                    self.send_listener_message(message)
                    print(message)
                return
            msg_dict = MessageSchema().loads(data)

            # Костыль если пришла история пробегамся по списку

            # Обычное получение
            message = msg_dict
            self.send_listener_message(message)
            print(data)

    def send_listener_message(self, message):
        if self.listener is not None:
            # Отдаем объект месседж
            self.listener.on_message(message)


if __name__ == '__main__':
    client = Client(None)
    client.listen()
    while True:
        msg = input("Введите сообщение: ")
        client.send_message(msg)
