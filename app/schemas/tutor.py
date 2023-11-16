from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto

class TutorIn(DefaultAuto):
    name = fields.String(required=True)
    lastname = fields.String(required=True)
    document = fields.String(required=False)
    username = fields.String(required=True)
    password = fields.String(required=False)
    email = fields.String(required=False)
    kinship = fields.String(required=True)
    phone = fields.String(required=False)
    regime = fields.String(required=False)
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
            f'{tutor["name"]} {tutor["lastname"]} - ' +
            f'{tutor["kinship"] if "kinship" in tutor else ""}')

class Tutors(Schema):
    items = fields.List(fields.Nested(TutorOut))