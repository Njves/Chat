from marshmallow import Schema, fields, post_load
import uuid


def generate_uid():
    return str(uuid.uuid4()).split("-")[0]


def from_json(json):
    schema = AccountSchema()
    return schema.loads(json)


class Account:
    def __init__(self, uid, name, email):
        self.uid = uid
        self.name = name
        self.email = email
        self.schema = AccountSchema()

    def to_json(self):
        return self.schema.dumps(self)

    def __repr__(self):
        return "Account(" + str(self.schema.dump(self)) + ")"


class AccountSchema(Schema):
    uid = fields.Str()
    name = fields.Str()
    email = fields.Str()

    @post_load
    def load(self, data, **kwargs):
        return Account(**data)
