from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto


class AdminIn(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
    username = fields.String()
    password = fields.String(required=False, load_default='')
    email = fields.String()
    status = fields.String(load_default='PENDING', allow_none=True)


class AdminOut(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
    username = fields.String()
    email = fields.String()
    status = fields.String()
    fullname = fields.Function(
        lambda admin: f'{admin["name"]} {admin["lastname"]}')


class Admins(Schema):
    items = fields.List(fields.Nested(AdminOut))