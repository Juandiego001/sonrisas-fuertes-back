from app.schemas.comment import CommentOut
from app.schemas.generic import DefaultAuto
from apiflask import Schema, fields
from app.schemas.link import LinkOut
from app.schemas.file import FileOut


class PublicationIn(DefaultAuto):
    title = fields.String()
    description = fields.String()
    status = fields.Boolean(required=False, load_default=True)
    links = fields.List(fields.String, required=False)
    files = fields.List(fields.File, required=False)


class PublicationOut(DefaultAuto):
    title = fields.String()
    description = fields.String()
    created_at = fields.String()
    fullname = fields.String()
    username = fields.String()
    status = fields.Boolean()
    comments = fields.List(fields.Nested(CommentOut))
    links = fields.List(fields.Nested(LinkOut))
    files = fields.List(fields.Nested(FileOut))


class Publications(Schema):
    items = fields.List(fields.Nested(PublicationOut))