import socket as sock
import sys
import threading
import configparser
import time
import msvcrt

from model.protocol import Protocol, from_json

print("ДоБрО пОжАлОвАтЬ нА сЕрВеР шИзОфРеНиЯ")


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
        self.is_start = True

    def on_connection(self, address, connection):
        print(str(address) + " is connected")
        print(self.message_history)

        if len(self.message_history) > 0:
            protocol = Protocol(Protocol.LIST, self.message_history)
            json_list = protocol.to_json() + "\n"
            connection.send(json_list.encode('utf-8'))

    def on_disconnect(self, address):
        print(str(address) + " has been disconnected")

    def start(self):
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

                protocol = from_json(data)
                print(protocol)
                if protocol.data_type == Protocol.DISCONNECT:
                    print("Клиент отключился")
                    print(self.message_history)
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


class Command:
    def __init__(self):
        pass


class ServerAdminConsole:
    def __init__(self, instance: Server):
        self.server = instance
        self.start_time = time.time()

    def get_start_time(self):
        return time.time() - self.start_time

    def execute_command(self, command):
        if command == "/time":
            print(self.get_start_time())

    def enter_command(self):
        self.execute_command(msvcrt.getch())


class CommandStorage:
    commands = ['/time', '/connections']

    def search_command(self, raw_query):
        if raw_query in self.commands:
            return


if __name__ == '__main__':
    server = Server()
    server.start()
