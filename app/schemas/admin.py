from apiflask import Schema, fields

class AdminIn(Schema):
    username = fields.String()
    password = fields.String()
    email = fields.String()