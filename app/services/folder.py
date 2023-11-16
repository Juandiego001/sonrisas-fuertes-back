from werkzeug.exceptions import HTTPException
from datetime import datetime
from app import mongo
from bson import ObjectId


def verify_folder_exists_by_id(folderid: str):
    return mongo.db.folders.find_one(ObjectId(folderid))


def verify_folder_exists(params: list):
    return mongo.db.folders.find_one({'$or': params})


def create_folder(params: dict):
    if verify_folder_exists([{'name': params['name']}]):
        raise HTTPException('La carpeta ya existe')
    params['updated_at'] = datetime.now()
    params['status'] = True
    return mongo.db.folders.insert_one(params)


def get_folders():
    return list(mongo.db.folders.find({}))


def get_folder_files(folderid: str):
    return mongo.db.files.find({'folderid': ObjectId(folderid)})


def get_folder_by_id(folderid: str):
    folder = verify_folder_exists_by_id(folderid)
    if not folder:
        raise HTTPException('Carpeta no encontrada')
    return folder

def get_folder_files_by_id(folderid: str):
    folder = verify_folder_exists_by_id(folderid)
    if not folder:
        raise HTTPException('Carpeta no encontrada')
    return get_folder_files(folderid)


def update_folder(folderid: str, params: dict):
    folder = verify_folder_exists_by_id(folderid)
    if not folder:
        raise HTTPException('Carpeta no encontrada')
    
    if 'name' in params and params['name'] != folder['name']:
        if verify_folder_exists([{'name': params['name']}]):
            raise HTTPException('La carpeta ya existe')
    
    params['updated_at'] = datetime.now()
    updated = mongo.db.folders.update_one({'_id': ObjectId(folderid)},
                                          {'$set': params})
    if not updated:
        raise HTTPException('La carpeta no fue actualizada')
    return updated
