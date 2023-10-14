from app.schemas.comment import Comments
from app.schemas.generic import DefaultAuto
from apiflask import Schema, fields


class PublicationIn(DefaultAuto):
    description = fields.String()

class PublicationOut(DefaultAuto):
    description = fields.String()
    created_at = fields.String()
    fullname = fields.String()
    username = fields.String()


class PublicationComment(DefaultAuto):
    description = fields.String()
    comments = fields.List(fields.Nested(Comments))

class Publications(Schema):
    items = fields.List(fields.Nested(PublicationOut))

class PublicationsComments(Schema):
    items = fields.List(fields.Nested(PublicationComment))