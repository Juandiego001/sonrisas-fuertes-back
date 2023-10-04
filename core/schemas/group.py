from apiflask import Schema, fields


class GroupIn(Schema):
    name = fields.String()