from apiflask import APIBlueprint, abort
from flask import send_file
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.file import FileIn, FileOut, Files
from app.services import file
from app.schemas.generic import Message
from werkzeug.exceptions import HTTPException
from dropbox.exceptions import HttpError
from app.utils import success_message


bp = APIBlueprint('file', __name__)


@bp.put('/')
@bp.input(FileIn, location='form_and_files')
@bp.output(Message)
@jwt_required()
def put_file(form_and_files_data):
    try:
        form_and_files_data['updated_by'] = get_jwt()['username']
        file.put_file(form_and_files_data)
        return success_message()
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Files)
def get_files():
    try:
        return Files().dump({'items': file.get_files()})
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:fileid>')
@bp.output(FileOut)
def get_file_detail(fileid):
    try:
        return file.get_file_detail(fileid)
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/download/<string:fileid>')
def download_file(fileid):
    try:
        file_data, real_name = file.download_file(fileid)
        return send_file(file_data,
                         as_attachment=True,
                         download_name=real_name)
    except HttpError as ex:
        abort(ex.status_code, ex.body)
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:fileid>')
@bp.input(FileIn)
@bp.output(Message)
@jwt_required()
def update_file(fileid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        file.update_file(fileid, data)
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))
    