from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from app.schemas.group import GroupIn, GroupOut, Groups
from app.services import group
from app.schemas.generic import Message

bp = APIBlueprint('group', __name__)

@bp.post('/')
@bp.input(GroupIn)
@bp.output(Message)
@jwt_required()
def create_group(data):
    try:
        data['updated_by'] = get_jwt()['username']
        group.create_group(data)
        return {'message': 'Grupo creado'}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/<string:groupid>')
@bp.output(GroupOut)
def get_group_detail(groupid):
    try:
        return group.get_group_by_id(groupid)
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/')
@bp.output(Groups)
def get_groups():
    try:
        return Groups().dump({'items': group.get_groups()})
    except Exception as ex:
        abort(500, str(ex))

@bp.patch('/<string:groupid>')
@bp.input(GroupIn)
@bp.output(Message)
@jwt_required()
def update_group(groupid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        group.update_group(groupid, data)
        return {'message': 'Grupo actualizado con éxito'}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

