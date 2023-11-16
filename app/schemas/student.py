from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId


class StudentIn(DefaultAuto):
    name = fields.String(required=True)
    lastname = fields.String(required=True)
    document = fields.String(required=False)
    username = fields.String(required=False)
    password = fields.String(required=False)
    email = fields.String(required=False)
    hospital = fields.String(required=False)
    born_at = fields.String(required=False)
    diagnosis = fields.String(required=False)
    eps = fields.String(required=False)
    gender = fields.String(required=False)
    godfather = fields.Boolean(required=False)
    tutorsid = fields.List(fields.String, required=False)
    city = fields.String(required=False)
    neighborhood = fields.String(required=False)
    address = fields.String(required=False)
    observations = fields.String(required=False)
    status = fields.String(load_default='PENDING', allow_none=True)


class StudentOut(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
    username = fields.String()
    email = fields.String()
    hospital = fields.String()
    born_at = fields.String()
    diagnosis = fields.String()
    eps = fields.String()
    gender = fields.String()
    godfather = fields.Boolean()
    tutorsid = fields.List(ObjectId)
    city = fields.String()
    neighborhood = fields.String()
    address = fields.String()
    observations = fields.String()
    status = fields.String()
    fullname = fields.Function(
        lambda student: f'{student["name"]} {student["lastname"]}')


class Students(Schema):
    items = fields.List(fields.Nested(StudentOut))
