from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.services import permission
from app.schemas.permission import Permission, Permissions
from app.schemas.generic import Message

bp = APIBlueprint('permission', __name__)

@bp.patch('/<string:permissionid>')
@bp.input(Permission)
@bp.output(Message)
@jwt_required()
def update_permission(permissionid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        permission.update_permission(permissionid, data)
        return {'message': 'Permission updated successfully'}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/<string:profileid>')
@bp.output(Permissions)
def get_permissions(profileid):
    try:
        return permission.get_permissions_by_profile(profileid)
    except Exception as ex:
        abort(500, ex.description)