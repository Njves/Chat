from client import Client


class ConsoleClient:
    def __init__(self):
        self.client = Client(self)


if __name__ == '__main__':
    ConsoleClient()