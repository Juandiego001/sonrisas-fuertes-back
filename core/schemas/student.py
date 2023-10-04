from apiflask import Schema, fields

class StudentIn(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.String(required=True)

class StudentOut(Schema):
    username = fields.String(dump_only=True)
    password = fields.String(dump_only=True)
    email = fields.String(dump_only=True)

class StudentsOut(Schema):
    students = fields.List(fields.Nested(StudentOut))