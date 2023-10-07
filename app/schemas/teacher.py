from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto

class TeacherIn(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
    username = fields.String()
    password = fields.String(required=False, load_default='')
    email = fields.String()
    status = fields.String(load_default='PENDING', allow_none=True)

class TeacherOut(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
    username = fields.String()
    email = fields.String()
    status = fields.String()
    fullname = fields.Function(
        lambda teacher: f'{teacher["name"]} {teacher["lastname"]}')

class Teachers(Schema):
    items = fields.List(fields.Nested(TeacherOut))