from http.client import HTTPException
from apiflask import APIBlueprint, abort
from app.schemas.student import StudentIn, StudentsOut
from app.services import student

bp = APIBlueprint('students', __name__)

@bp.get('/')
@bp.output(StudentsOut)
def get_students(params):
    try:
        students = student.get_students()
        return students
    except Exception as ex:
        abort(500, str(ex))

# @bp.post('/')
# @bp.input(StudentIn)
# def create_user(user_data):
#     try:
#         users.append(user_data)
#         return {'message': 'User created successfully'}
#     except Exception as ex:
#         abort(500, str(ex))

