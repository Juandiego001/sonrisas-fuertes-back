from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.folder import FolderIn, FolderOut, FolderFilesOut, Folders
from app.services import folder
from app.schemas.generic import Message
from werkzeug.exceptions import HTTPException
from app.utils import success_message


bp = APIBlueprint('folder', __name__)


@bp.post('/')
@bp.input(FolderIn)
@bp.output(Message)
@jwt_required()
def create_folder(data):
    try:
        data['updated_by'] = get_jwt()['username']
        folder.create_folder(data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Folders)
def get_folders():
    try:
        return Folders().dump({'items': folder.get_folders()})
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:folderid>')
@bp.output(FolderOut)
def get_folder_detail(folderid):
    try:
        return FolderOut().dump(folder.get_folder_by_id(folderid))
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/folder/files/<string:folderid>')
@bp.output(FolderFilesOut)
def get_files_of_folder(folderid):
    try:
        return FolderFilesOut().dump({'items': 
                                      folder.get_folder_files_by_id(folderid)})
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:folderid>')
@bp.input(FolderIn)
@bp.output(Message)
@jwt_required()
def update_folder(folderid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        folder.update_folder(folderid, data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))
