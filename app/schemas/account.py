from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto


class Login(Schema):
    password = fields.String()
    username = fields.String()

class Email(Schema):
    email = fields.String()

class Password(Schema):
    password = fields.String()

class Ability(Schema):
    subject = fields.String()
    action = fields.String()

class Profile(DefaultAuto):
    abilities = fields.List(fields.Nested(Ability))
    username = fields.String()
    name = fields.String()
    lastname = fields.String()
    document = fields.Integer()

class Photo(Schema):
    photo = fields.File()

