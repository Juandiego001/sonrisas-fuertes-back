from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto
from app.schemas.permission import PermissionOut


class ProfileIn(DefaultAuto):
    name = fields.String()
    status = fields.String(required=False, load_default='ACTIVE')


class ProfileOut(DefaultAuto):
    name = fields.String(dump_only=True)
    status = fields.String(dump_only=True)
    permissions = fields.List(fields.Nested(PermissionOut))


class Profiles(Schema):
    items = fields.List(fields.Nested(ProfileOut))