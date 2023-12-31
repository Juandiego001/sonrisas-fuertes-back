from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.student import StudentIn, StudentOut, Students
from app.services import student
from app.schemas.generic import Message
from app.utils import success_message


bp = APIBlueprint('student', __name__)


@bp.post('/')
@bp.input(StudentIn)
@bp.output(Message)
@jwt_required()
def create_student(data):
    try:
        data['updated_by'] = get_jwt()['username']
        student.create_student(data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:studentid>')
@bp.output(StudentOut)
def get_student_detail(studentid):
    try:
        return student.get_student_by_id(studentid)
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Students)
def get_students():
    try:
        return Students().dump({'items': student.get_students()})
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:studentid>')
@bp.input(StudentIn)
@bp.output(Message)
@jwt_required()
def update_student(studentid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        student.update_student(studentid, data)
        return success_message()
    except HTTPException as ex:        
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))
