from apiflask import fields
from app.schemas.generic import DefaultAuto, ObjectId


class AttachmentOut(DefaultAuto):
    commentid = ObjectId()
    publicationid = ObjectId()
    folderid = ObjectId()
    hash_name = fields.String()
    real_name = fields.String()
    url = fields.String()
    isLink = fields.Boolean()
    status = fields.Boolean()