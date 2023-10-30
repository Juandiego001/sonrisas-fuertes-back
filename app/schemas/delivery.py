from apiflask import fields, Schema
from app.schemas.generic import DefaultAuto, ObjectId
from app.schemas.link import LinkIn, LinkOut
from app.schemas.file import FileOut


class DeliveryIn(DefaultAuto):
    activityid = ObjectId()
    description = fields.String()
    status = fields.Boolean()
    links = fields.List(fields.Nested(LinkIn), required=False)
    files = fields.List(fields.File, required=False)


class DeliveryOut(DefaultAuto):
    description = fields.String()
    created_at = fields.String()
    status = fields.Boolean()
    username = fields.String()
    fullname = fields.String()
    links = fields.List(fields.Nested(LinkOut))
    files = fields.List(fields.Nested(FileOut))


class Deliveries(Schema):
    items = fields.List(fields.Nested(DeliveryOut))