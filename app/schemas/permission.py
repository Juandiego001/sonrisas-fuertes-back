from app.schemas.generic import DefaultAuto
from apiflask import Schema, fields
from app.schemas.generic import ObjectId


class PermissionIn(DefaultAuto):
    read = fields.Boolean()
    update = fields.Boolean()
    create = fields.Boolean()
    delete = fields.Boolean()


class PermissionInCreate(PermissionIn):
    profileid = ObjectId()
    moduleid = ObjectId()


class PermissionOut(DefaultAuto):
    read = fields.Boolean()
    update = fields.Boolean()
    create = fields.Boolean()
    delete = fields.Boolean()
    module = fields.String()


class Permissions(Schema):
    items = fields.List(fields.Nested(PermissionOut))
