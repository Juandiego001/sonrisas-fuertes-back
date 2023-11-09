from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId


class PatientIn(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
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
    status = fields.String(load_default='ACTIVE', allow_none=True)


class PatientOut(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
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


class Patients(Schema):
    items = fields.List(fields.Nested(PatientOut))
