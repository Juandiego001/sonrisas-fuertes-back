from apiflask import fields, Schema
from app.schemas.generic import DefaultAuto, ObjectId

class CommentIn(DefaultAuto):
    publicationid = ObjectId()
    description = fields.String()
    status = fields.Boolean()

class CommentOut(DefaultAuto):
    description = fields.String()
    created_at = fields.String()
    status = fields.Boolean()
    username = fields.String()
    fullname = fields.String()

class Comments(Schema):
    items = fields.List(fields.Nested(CommentOut))