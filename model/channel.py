import uuid


class Channel:
    def __init__(self, uid, name, connection_size):
        self.uid = uid
        self.name = name
        self.connection_size = connection_size
        self.message_list = []



