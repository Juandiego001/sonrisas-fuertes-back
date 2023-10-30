from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId

class LinkIn(DefaultAuto):
    folderid = ObjectId(required=False, load_default=None)
    activityid = ObjectId(required=False, load_default=None)
    publicationid = ObjectId(required=False, load_default=None)
    commentid = ObjectId(required=False, load_default=None)
    deliveryid = ObjectId(required=False, load_default=None)
    shortcut = fields.String()
    url = fields.String()
    status = fields.Boolean(required=False)


class LinkOut(DefaultAuto):
    folderid = ObjectId()
    activityid = ObjectId()
    publicationid = ObjectId()
    commentid = ObjectId()
    deliveryid = ObjectId()
    shortcut = fields.String()
    url = fields.String()
    status = fields.Boolean()


class Links(Schema):
    items = fields.List(fields.Nested(LinkOut))
