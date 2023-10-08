from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto


class GroupIn(DefaultAuto):
    name = fields.String()
    status = fields.Boolean(load_default=True, allow_none=True)

class GroupOut(DefaultAuto):
    name = fields.String()
    status = fields.Boolean()

class Groups(Schema):
    items = fields.List(fields.Nested(GroupOut))