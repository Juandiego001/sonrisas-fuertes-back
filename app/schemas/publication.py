from app.schemas.comment import CommentOut
from app.schemas.generic import DefaultAuto
from apiflask import Schema, fields


class PublicationIn(DefaultAuto):
    title = fields.String()
    description = fields.String()
    isActivity = fields.Boolean(required=False, load_default=False)
    status = fields.Boolean(required=False, load_default=True)

class PublicationOut(DefaultAuto):
    title = fields.String()
    description = fields.String()
    created_at = fields.String()
    fullname = fields.String()
    username = fields.String()
    status = fields.Boolean()
    isActivity = fields.Boolean()
    comments = fields.List(fields.Nested(CommentOut))

class Publications(Schema):
    items = fields.List(fields.Nested(PublicationOut))