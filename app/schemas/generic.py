from apiflask import Schema, fields
import bson
from marshmallow import EXCLUDE, ValidationError, missing
from apiflask.validators import Length

class ObjectId(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return bson.ObjectId(value)
        except Exception:
            raise ValidationError(f'Invalid ObjectId {value}')

    def _serialize(self, value, attr, obj):
        if value is None:
            return missing
        return str(value)

class DefaultAuto(Schema):

    class Meta:
        unknown = EXCLUDE

    _id = ObjectId(dump_only=True)
    updated_by = fields.String(dump_only=True, validate=[Length(0, 100)])
    updated_at = fields.String(dump_only=True)

class Message(Schema):
    message = fields.String()
    data = fields.Dict()
