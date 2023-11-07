from app.schemas.generic import DefaultAuto
from apiflask import Schema, fields


class PermissionIn(DefaultAuto):
    read = fields.Boolean()
    update = fields.Boolean()
    create = fields.Boolean()


class PermissionOut(DefaultAuto):
    read = fields.Boolean()
    update = fields.Boolean()
    create = fields.Boolean()
    module = fields.String()


class Permissions(Schema):
    items = fields.List(fields.Nested(PermissionOut))
