from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto

class StudentIn(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
    username = fields.String()
    password = fields.String(required=False, load_default='')
    email = fields.String()
    status = fields.String(required=False, load_default='PENDING')

class StudentOut(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
    username = fields.String()
    email = fields.String()
    status = fields.String(required=False)
    fullname = fields.Function(
        lambda student: f'{student["name"]} {student["lastname"]}')

class Students(Schema):
    items = fields.List(fields.Nested(StudentOut))
