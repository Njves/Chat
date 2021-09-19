from marshmallow import Schema, fields, post_load

from model.message import MessageSchema, Message


def from_json(json):
    return ProtocolSchema().loads(json)


class Protocol:
    SHOT = "shot"
    LIST = "list"
    ATTACH = "attach"
    ON_CONNECT = "on_connect"
    DISCONNECT = "disconnect"

    def __init__(self, data_type, content):
        self.data_type = data_type
        self.content = content

    def to_json(self):
        return ProtocolSchema().dumps(self)

    def __repr__(self):
        return str({"data_type": self.data_type, "content": self.content})


class ProtocolSchema(Schema):
    data_type = fields.Str()
    content = fields.List(fields.Nested(MessageSchema))

    @post_load
    def load(self, data, **kwargs):
        return Protocol(**data)
