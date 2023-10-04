from apiflask import Schema, fields


class Message(Schema):
    message = fields.String()
    data = fields.Dict()