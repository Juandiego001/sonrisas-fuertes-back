from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.generic import Message
from app.schemas.module import ModuleIn, ModuleOut, Modules
from app.services import module
from app.utils import success_message


bp = APIBlueprint('module', __name__)


@bp.post('/')
@bp.input(ModuleIn)
@bp.output(Message)
@jwt_required()
def create_module(data):
  try:
    data['updated_by'] = get_jwt()['username']
    module.create_module(data)
    return success_message()
  except HTTPException as ex:
    abort(400, ex.description)
  except Exception as ex:
    abort(500, str(ex))


@bp.get('/')
@bp.output(Modules)
@jwt_required()
def get_modules():
  try:
    return Modules().dump({'items': module.get_modules()})
  except Exception as ex:
    abort(500, str(ex))


@bp.get('/<string:moduleid>')
@bp.output(ModuleOut)
@jwt_required()
def get_module_detail(moduleid):
  try:
    return module.get_module_by_id(moduleid)
  except Exception as ex:
    abort(500, str(ex))


@bp.patch('/<string:moduleid>')
@bp.input(ModuleIn)
@bp.output(Message)
@jwt_required()
def update_module(moduleid, data):
  try:
    data['updated_by'] = get_jwt()['username']
    module.update_module(moduleid, data)
    return success_message()
  except HTTPException as ex:
    abort(400, ex.description)
  except Exception as ex:
    abort(500, str(ex))
