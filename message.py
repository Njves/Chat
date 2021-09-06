import time
import json
from json import JSONEncoder
from marshmallow import Schema, fields, post_load


# Протокол сообщений внутри приложения
class Message:

    def __init__(self, text, sender, date=None, id=None):

        self.date = time.time()
        self.text = text
        self.sender = sender

    # def to_json(self):
    #     struct = {"date": self.date, "text": self.text}
    #     return json.dumps(struct, ensure_ascii=False)

    def to_json(self):
        schema = MessageSchema()
        format_json = str(schema.dump(self)).replace("\'", "\"")
        format_json += "\n"
        return format_json

    def to_dict(self):
        return {"date": self.date, "text": self.text, "sender": self.sender}

    def __str__(self):
        return self.to_dict().__str__()

    def __repr__(self) -> str:
        return self.to_dict().__str__()


class MessageSchema(Schema):
    date = fields.Str()
    text = fields.Str()
    sender = fields.Str()

    @post_load
    def load(self, data, **kwargs):
        return Message(**data)


