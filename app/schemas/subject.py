from apiflask import fields, Schema
from app.schemas.generic import DefaultAuto


class SubjectIn(DefaultAuto):
    name = fields.String()

class SubjectOut(DefaultAuto):
    name = fields.String()

class Subjects(Schema):
    items = fields.List(fields.Nested(SubjectOut))