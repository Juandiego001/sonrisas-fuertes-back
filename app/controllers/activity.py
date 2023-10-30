import json
from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from app.schemas.activity import ActivityIn, ActivityOut, Activities
from app.services import activity
from app.schemas.generic import Message
from app.utils import success_message


bp = APIBlueprint('activity', __name__)


@bp.post('/')
@bp.input(ActivityIn, location='files')
@bp.output(Message)
@jwt_required()
def create_activity(files_data):
    '''
    Create activity
    :param data:
    '''
    try:
        files_data['userid'] = get_jwt()['_id']
        if 'links' in files_data:
            files_data['links'] = \
                [json.loads(link) for link in files_data['links']]
        files_data['updated_by'] = get_jwt()['username']
        activity.create_activity(files_data)
        return success_message()
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Activities)
def get_activites():
    '''
    Get activities
    '''
    try:
        return Activities().dump({'items': activity.get_activities()})
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:activityid>')
@bp.output(ActivityOut)
@jwt_required()
def get_activity_detail(activityid):
    '''
    Get activity detail
    '''
    try:
        return activity.get_activity_by_id(
            activityid, get_jwt()['username']).next()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:activityid>')
@bp.input(ActivityIn, location='form_and_files')
@bp.output(Message)
@jwt_required()
def update_activity(activityid, files_data):
    '''
    Update activity
    :param data:
    '''
    try:
        if 'links' in files_data:
            files_data['links'] = \
                [json.loads(link) for link in files_data['links']]
        files_data['updated_by'] = get_jwt()['username']
        activity.update_activity(activityid, files_data)
        return success_message()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))