from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId

class StudentIn(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
    username = fields.String()
    password = fields.String(required=False, load_default='')
    email = fields.String()
    groupid = ObjectId()
    status = fields.String(load_default='PENDING', allow_none=True)

class StudentOut(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
    username = fields.String()
    email = fields.String()
    status = fields.String()
    groupid = ObjectId()
    fullname = fields.Function(
        lambda student: f'{student["name"]} {student["lastname"]}')

class StudentsByGroup(Schema):
    groupid = fields.String(load_default='')

class Students(Schema):
    items = fields.List(fields.Nested(StudentOut))
