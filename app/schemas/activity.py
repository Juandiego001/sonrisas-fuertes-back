from app.schemas.delivery import DeliveryOut
from app.schemas.generic import DefaultAuto
from apiflask import Schema, fields
from app.schemas.link import LinkOut
from app.schemas.file import FileOut


class ActivityIn(DefaultAuto):
    title = fields.String()
    description = fields.String()
    status = fields.Boolean(required=False)
    links = fields.List(fields.String, required=False)
    files = fields.List(fields.File, required=False)


class ActivityOut(DefaultAuto):
    title = fields.String()
    description = fields.String()
    created_at = fields.String()
    fullname = fields.String()
    username = fields.String()
    status = fields.Boolean()
    delivery = fields.Nested(DeliveryOut)
    links = fields.List(fields.Nested(LinkOut))
    files = fields.List(fields.Nested(FileOut))


class Activities(Schema):
    items = fields.List(fields.Nested(ActivityOut))