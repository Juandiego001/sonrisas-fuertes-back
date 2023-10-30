from apiflask import fields, Schema
from app.schemas.generic import DefaultAuto, ObjectId
from app.schemas.attachment import AttachmentOut

class CommentIn(DefaultAuto):
    publicationid = ObjectId()
    description = fields.String()
    status = fields.Boolean()
    files = fields.List(fields.File, required=False)
    links = fields.List(fields.String, required=False)

class CommentOut(DefaultAuto):
    description = fields.String()
    created_at = fields.String()
    status = fields.Boolean()
    username = fields.String()
    fullname = fields.String()
    attachments = fields.List(fields.Nested(AttachmentOut))

class Comments(Schema):
    items = fields.List(fields.Nested(CommentOut))