from apiflask import fields, Schema
from app.schemas.generic import DefaultAuto
from app.schemas.file import FileOut


class FolderIn(DefaultAuto):
    name = fields.String()
    status = fields.Boolean(required=False, load_default=True)


class FolderOut(DefaultAuto):
    name = fields.String()
    status = fields.Boolean()


class FolderFilesOut(DefaultAuto):
    items = fields.List(fields.Nested(FileOut))


class Folders(Schema):
    items = fields.List(fields.Nested(FolderOut))
