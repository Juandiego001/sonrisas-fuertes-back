from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.tutor import TutorIn, TutorOut, Tutors
from app.schemas.generic import Message
from app.services import tutor
from app.utils import success_message


bp = APIBlueprint('tutor', __name__)


@bp.post('/')
@bp.input(TutorIn)
@bp.output(Message)
@jwt_required()
def create_tutor(data):
    try:
        data['updated_by'] = get_jwt()['username']
        tutor.create_tutor(data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:tutorid>')
@bp.output(TutorOut)
def get_tutor_detail(tutorid):
    try:
        return tutor.get_tutor_by_id(tutorid)
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Tutors)
def get_tutors():
    try:
        return Tutors().dump({'items': tutor.get_tutors()})
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:tutorid>')
@bp.input(TutorIn)
@bp.output(Message)
@jwt_required()
def update_tutor(tutorid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        tutor.update_tutor(tutorid, data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

