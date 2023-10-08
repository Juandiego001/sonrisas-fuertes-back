from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.admin import AdminIn, AdminOut, Admins
from app.schemas.generic import Message
from app.services import admin

bp = APIBlueprint('admin', __name__)

@bp.post('/')
@bp.input(AdminIn)
@bp.output(Message)
@jwt_required()
def create_admin(data):
    try:
        data['updated_by'] = get_jwt()['username']
        admin.create_admin(data)
        return {'message': 'Admin created successfully'}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/<string:adminid>')
@bp.output(AdminOut)
def get_admin_detail(adminid):
    try:
        return admin.get_admin_by_id(adminid)
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/')
@bp.output(Admins)
def get_admins():
    try:
        return Admins().dump({'items': admin.get_admins()})
    except Exception as ex:
        abort(500, str(ex))

@bp.patch('/<string:adminid>')
@bp.input(AdminIn)
@bp.output(Message)
@jwt_required()
def update_admin(adminid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        admin.update_admin(adminid, data)
        return {'message': 'Admin updated successfully'}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

