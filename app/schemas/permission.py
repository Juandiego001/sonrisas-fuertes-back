from app.schemas.generic import DefaultAuto
from apiflask import Schema, fields
from app.schemas.module import ModuleOut

class Permission(DefaultAuto):
    read = fields.Boolean()
    update = fields.Boolean()
    create = fields.Boolean()
    module = fields.Nested(ModuleOut)


class Permissions(Schema):
    items = fields.List(fields.Nested(Permission))
