from apiflask import APIBlueprint, abort
from flask import send_file
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.folder import FolderIn, FolderOut, Folders, FolderFileIn,\
    FolderFiles
from app.services import folder
from app.schemas.generic import Message
from werkzeug.exceptions import HTTPException
from dropbox.exceptions import HttpError

bp = APIBlueprint('folder', __name__)

@bp.post('/')
@bp.input(FolderIn)
@bp.output(Message)
@jwt_required()
def create_folder(data):
    try:
        data['updated_by'] = get_jwt()['username']
        folder.create_folder(data)
        return {'message': 'Carpeta creada con éxito'}
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

@bp.patch('/<string:folderid>')
@bp.input(FolderIn)
@bp.output(Message)
@jwt_required()
def update_folder(folderid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        folder.update_folder(folderid, data)
        return {'message': 'Carpeta actualizada con éxito'}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.put('/files/<string:folderid>')
@bp.input(FolderFileIn, location='files')
@jwt_required()
def upload_file_for_folder(folderid, files):
    try:        
        
        folder.upload_file(folderid, files['file'], get_jwt()['username'])
        return {'message': 'Archivo subido exitosamente'}
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/files/<string:folderid>')
@bp.output(FolderFiles)
def get_files(folderid):
    try:
        return FolderFiles().dump({'items': folder.get_files(folderid)})
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/files/<string:folderid>/<string:hash_name>')
def download_file(folderid, hash_name):
    try:
        return send_file(folder.download_file(folderid, hash_name),
                         as_attachment=True,
                         download_name=hash_name)
    except HttpError as ex:
        abort(ex.status_code, ex.body)
    except Exception as ex:
        abort(500, str(ex))
