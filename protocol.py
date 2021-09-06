from marshmallow import Schema, fields, post_load

from message import Message, MessageSchema


class Protocol:

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