from apiflask import fields, Schema
from app.schemas.generic import DefaultAuto, ObjectId
from app.schemas.file import FileOut
from app.schemas.link import LinkOut

class CommentIn(DefaultAuto):
    publicationid = ObjectId()
    description = fields.String()
    status = fields.Boolean()
    links = fields.List(fields.String, required=False)
    files = fields.List(fields.File, required=False)

class CommentOut(DefaultAuto):
    description = fields.String()
    created_at = fields.String()
    status = fields.Boolean()
    username = fields.String()
    fullname = fields.String()
    links = fields.List(fields.Nested(LinkOut))
    files = fields.List(fields.Nested(FileOut))

class Comments(Schema):
    items = fields.List(fields.Nested(CommentOut))