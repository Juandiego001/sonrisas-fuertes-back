from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId

class FileIn(DefaultAuto):
    folderid = ObjectId(required=False, load_default=None)
    activityid = ObjectId(required=False, load_default=None)
    publicationid = ObjectId(required=False, load_default=None)
    commentid = ObjectId(required=False, load_default=None)
    deliveryid = ObjectId(required=False, load_default=None)
    file = fields.File()
    status = fields.Boolean(required=False)


class FileOut(DefaultAuto):
    folderid = ObjectId()
    activityid = ObjectId()
    publicationid = ObjectId()
    commentid = ObjectId()
    deliveryid = ObjectId()
    hash_name = fields.String()
    real_name = fields.String()
    url = fields.String()
    status = fields.Boolean()


class Files(Schema):
    items = fields.List(fields.Nested(FileOut))


