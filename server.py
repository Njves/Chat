import socket as sock
import threading
import configparser
import json

from message import Message, MessageSchema
from protocol import ProtocolSchema, Protocol


class Server:
    CONFIG = 'server_config.ini'

    def __init__(self):
        # Инициализация конфга
        self.cfg_parser = configparser.ConfigParser()
        # Список текущих подключений
        self.current_connections = []

        # Флаг работы сервера
        self.is_start = False

        # Инициализация сокета
        self.socket = sock.socket()
        # биндим к машине
        self.socket.bind(('', self.get_port()))
        # Количество подключений
        self.socket.listen(self.get_listen_size())
        # История чата
        self.message_history = []

    # Получить порт из конфига
    def get_port(self):
        self.cfg_parser.read(self.CONFIG)
        return int(self.cfg_parser['server']['port'])

    def get_listen_size(self):
        self.cfg_parser.read(self.CONFIG)
        return int(self.cfg_parser['server']['listen_size'])

    def on_start(self):
        print("Server is starting")

    def on_connection(self, address, connection):
        print(str(address) + " is connected")
        print(self.message_history)

        if len(self.message_history) > 0:

            protocol = Protocol("list", self.message_history)
            protocol_schema = ProtocolSchema()

            json_list = protocol_schema.dumps(protocol)
            json_list = json_list + "\n"
            connection.send(json_list.encode('utf-8'))

    def on_disconnect(self, address):
        print(str(address) + " has been disconnected")

    def start(self):
        self.is_start = True
        self.on_start()
        while self.is_start:
            connection, address = self.socket.accept()
            self.on_connection(address, connection)
            if not (connection in self.current_connections):
                self.current_connections.append(connection)
                thread = threading.Thread(target=self.talking, args=(connection, address, self.current_connections))
                thread.start()

    def talking(self, connection, address, connection_list):
        while True:
            try:
                # Получаем сырые данные от клиента
                data = connection.recv(4096).decode('utf-8')
                # Если сообщение не пустое выводим в лог
                if not data:
                    return
                print(f"info from {str(address)}" + ' raw_text: ' + data)
                # Парсим json в объект

                schema = ProtocolSchema()
                protocol = schema.loads(data)
                print(protocol)

                # Добавляем сообщения в историю, чтобы в случае отдать

                # Пробегаем по списку подключений отправляем всем сообщение
                for child_connection in connection_list:
                    # Пропускаем отправителя
                    if child_connection == connection:
                        self.message_history.append(protocol.content[0])
                        continue

                    child_connection.send(protocol.to_json().encode())
            except ConnectionResetError as e:
                # Если случилась ошибка сообщаем об отключение
                self.on_disconnect(address)
                # Отрубаем ишака
                connection_list.remove(connection)
                break


if __name__ == '__main__':
    server = Server()
    server.start()
