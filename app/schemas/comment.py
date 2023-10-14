from apiflask import fields, Schema
from app.schemas.generic import DefaultAuto

class CommentIn(Schema):
    description = fields.String()

class CommentOut(DefaultAuto):
    description = fields.String()

class Comments(Schema):
    items = fields.List(fields.Nested(CommentOut))