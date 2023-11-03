from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto

class TutorIn(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
    username = fields.String()
    password = fields.String(required=False, load_default='')
    email = fields.String()
    kinship = fields.String()
    phone = fields.String()
    regime = fields.String()
    status = fields.String(load_default='PENDING', allow_none=True)

class TutorOut(DefaultAuto):
    name = fields.String()
    lastname = fields.String()
    document = fields.String()
    username = fields.String()
    email = fields.String()
    kinship = fields.String()
    phone = fields.String()
    regime = fields.String()
    status = fields.String()
    fullname = fields.Function(
        lambda tutor: f'{tutor["name"]} {tutor["lastname"]}')
    full_relationship = fields.Function(
        lambda tutor:
            f'{tutor["name"]} {tutor["lastname"]} - {tutor["kinship"]}')

class Tutors(Schema):
    items = fields.List(fields.Nested(TutorOut))