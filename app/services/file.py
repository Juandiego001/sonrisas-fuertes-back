import io
import hashlib
from werkzeug.utils import secure_filename
from app import mongo, dbx
from app.utils import generate_id
from bson import ObjectId
from werkzeug.exceptions import HTTPException
from datetime import datetime
from app.services import folder
from app.services import activity
from app.services import publication
from app.services import comment
from app.services import delivery


def verify_file_exists(fileid: str):
    return mongo.db.files.find_one(ObjectId(fileid))


def get_dbx_folder(params: dict):
    if ('folderid' in params):
        return 'folders', str(params['folderid']),\
            folder.verify_folder_exists_by_id
    if ('activityid' in params):
        return 'activities', str(params['activityid']),\
            activity.verify_activity_exists
    if ('publicationid' in params):
        return 'publications', str(params['publicationid']),\
            publication.verify_publication_exists
    if ('commentid' in params):
        return 'comments', str(params['commentid']),\
            comment.verify_comment_exists
    if ('deliveryid' in params):
        return 'deliveries', str(params['deliveryid']),\
            delivery.verify_delivery_exists


def put_file(params: dict):
    file = params.pop('file')
    filename = secure_filename(file.filename)
    format = filename.split('.')[-1]
    hash_name = (f'{hashlib.sha1(generate_id().encode("utf-8")).hexdigest()}.'
                 f'{format}')    
    dbx_folder_name, dbx_folder_id, verify_function = get_dbx_folder(params)
    if not verify_function(dbx_folder_id):
        raise HTTPException('No se encontró el motivo asociado a este archivo')
    dbx.files_upload(file.read(),
                     f'/{dbx_folder_name}/{dbx_folder_id}/{hash_name}')
    
    params['url'] = f'{hash_name}?v={generate_id()}'
    params['hash_name'] = hash_name
    params['real_name'] = filename
    params['status'] = True
    params['created_at'] = params['updated_at'] = datetime.now()
    return mongo.db.files.insert_one(
        {key:value for key, value in params.items() if key != '_id'})


def put_files(params: dict):
    files = params.pop('files')
    for file in files:
        params['file'] = file
        inserted = put_file(params)
        if not inserted:
            raise HTTPException('El archivo no fue ingresado')



def get_files():
    return list(mongo.db.files.find({}))


def get_file_detail(fileid: str):
    file = verify_file_exists(fileid)
    if not file:
        raise HTTPException('Archivo no encontrado')
    return file


def download_file(fileid: str):
    params_file = verify_file_exists(fileid)
    if not params_file:
        raise HTTPException('Archivo no encontrado')
    dbx_folder_name, dbx_folder_id, _ = get_dbx_folder(params_file)
    md, file = dbx.files_download(
        f'/{dbx_folder_name}/{dbx_folder_id}/{params_file["hash_name"]}')
    return io.BytesIO(file.content), params_file['real_name']


def update_file(fileid: str, params: dict):
    file = verify_file_exists(fileid)
    if not file:
        raise HTTPException('Archivo no encontrado')
    params['updated_at'] = datetime.now()
    updated = mongo.db.files.update_one({'_id': ObjectId(fileid)},
                                        {'$set': params})
    if not updated:
        raise HTTPException('El archivo no fue actualizado')
    return updated


def delete_file(fileid: str):
    file = verify_file_exists(fileid)
    if not file:
        raise HTTPException('Archivo no encontrado')
    dbx_folder_name, dbx_folder_id, _ = get_dbx_folder(file)
    was_deleted = dbx.files_delete(
        f'/{dbx_folder_name}/{dbx_folder_id}/{file["hash_name"]}')
    if not was_deleted:
        raise HTTPException('Archivo no eliminado')
    was_deleted = mongo.db.files.delete_one({'_id': ObjectId(fileid)})
    if not was_deleted:
        raise HTTPException('Archivo no eliminado de la base de datos')
    return was_deleted

