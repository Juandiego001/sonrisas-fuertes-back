import io
import hashlib
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from datetime import datetime
from app import mongo, dbx
from bson import ObjectId

from app.utils import generate_id


def create_folder(params: dict):
    if verify_exists([{'name': params['name']}]):
        raise HTTPException('La carpeta ya ha sido creada')
    params['updated_at'] = datetime.now()
    return mongo.db.folders.insert_one(params)
    
def verify_exists(params: list):
    return mongo.db.folders.find_one({'$or': params})

def get_folders():
    return list(mongo.db.folders.find({}))

def get_folder_by_id(folderid: str):
    folder = verify_exists([{'_id': ObjectId(folderid)}])
    if not folder:
        raise HTTPException('La carpeta no existe')
    print('folder******', folder)
    return folder

def update_folder(folderid: str, params: dict):
    folder = verify_exists([{'_id': ObjectId(folderid)}])
    if not folder:
        raise HTTPException('La carpeta no existe')
    
    if 'name' in params and params['name'] != folder['name']:
        if verify_exists([{'name': params['name']}]):
            raise HTTPException('La carpeta ya ha sido creada')
    
    params['updated_at'] = datetime.now()
    updated = mongo.db.folders.update_one({'_id': ObjectId(folderid)},
                                          {'$set': params})
    if not updated:
        raise HTTPException('La carpeta no fue actualizada')
    return updated

def upload_file(folderid, file, updated_by):
    filename = secure_filename(file.filename)
    format = filename.split('.')[-1]
    hash_name = (f'{hashlib.sha1(generate_id().encode("utf-8")).hexdigest()}.'
                 f'{format}')
    data = file.read()
    dbx.files_upload(data, f'/materials/{folderid}/{hash_name}')
    url = f'{hash_name}?v={generate_id()}'
    return mongo.db.attachments.insert_one({
        'folderid': ObjectId(folderid),
        'publicationid': None,
        'hash_name': hash_name,
        'real_name': filename,
        'url': url,
        'status': True,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'updated_by': updated_by
    })

def get_files(folderid: str):
    return list(mongo.db.attachments.find({'folderid': ObjectId(folderid)}))

def download_file(folderid: str, hash_name: str):
    md, file = dbx.files_download(f'/materials/{folderid}/{hash_name}')
    return io.BytesIO(file.content)
