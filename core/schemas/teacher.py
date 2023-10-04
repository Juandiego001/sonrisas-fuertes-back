from apiflask import Schema, fields

class TeacherIn(Schema):
    username = fields.String()
    password = fields.String()
    email = fields.String()