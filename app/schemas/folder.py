from apiflask import fields, Schema
from app.schemas.generic import DefaultAuto, ObjectId

class FolderIn(DefaultAuto):
    name = fields.String()
    status = fields.Boolean(required=False, load_default=True)

class FolderOut(DefaultAuto):
    name = fields.String()
    status = fields.Boolean()

class Folders(Schema):
    items = fields.List(fields.Nested(FolderOut))
