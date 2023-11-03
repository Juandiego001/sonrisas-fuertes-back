from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId


class StudentIn(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
    username = fields.String()
    password = fields.String(required=False, load_default='')
    email = fields.String()
    hospital = fields.String()
    born_at = fields.String()
    diagnosis = fields.String()
    eps = fields.String()
    gender = fields.String()
    godfather = fields.Boolean()
    tutorsid = fields.List(fields.String, required=False)
    city = fields.String()
    neighborhood = fields.String()
    address = fields.String()
    observations = fields.String()    
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
