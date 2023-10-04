from apiflask import Schema, fields


class Login(Schema):
    password = fields.String()
    username = fields.String()

class Email(Schema):
    email = fields.String()

class Profile(Schema):
    username = fields.String()
    name = fields.String()
    lastname = fields.String()
    document = fields.Integer()

class Photo(Schema):
    photo = fields.File()

