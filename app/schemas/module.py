from apiflask import fields, Schema
from app.schemas.generic import DefaultAuto

class ModuleOut(DefaultAuto):
    name = fields.String()
    status = fields.Boolean()

class Modules(Schema):
    items = fields.List(fields.Nested(ModuleOut))