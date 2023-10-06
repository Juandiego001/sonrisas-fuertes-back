from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.teacher import TeacherIn, TeacherOut, Teachers
from app.schemas.generic import Message
from app.services import teacher

bp = APIBlueprint('teachers', __name__)

@bp.post('/')
@bp.input(TeacherIn)
@bp.output(Message)
@jwt_required()
def create_teacher(data):
    try:
        data['updated_by'] = get_jwt()['username']
        teacher.create_teacher(data)
        return {'message': 'Teacher created successfully'}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/<string:teacherid>')
@bp.output(TeacherOut)
def get_teacher_detail(teacherid):
    try:
        return teacher.get_teacher_by_id(teacherid)
    except HTTPException as ex:
        abort(401, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/')
@bp.output(Teachers)
def get_teachers():
    try:
        test = teacher.get_teachers()
        print('teachers*******', test)
        teachers = Teachers().dump({'items': test})
        return teachers
    except Exception as ex:
        abort(500, str(ex))

@bp.patch('/<string:teacherid>')
@bp.input(TeacherIn)
@bp.output(Message)
def update_teacher(teacherid, data):
    try:
        teacher.update_teacher(teacherid, data)
        return {'message': 'Teacher updated successfully'}
    except Exception as ex:
        abort(500, str(ex))

