from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId

def create_group(params: dict):
    group = verify_if_group_exists(params['name'])
    if group:
        raise HTTPException('El grupo ya existe')
    params['status'] = True
    params['updated_at'] = datetime.now()
    return mongo.db.curso.insert_one(params)

def get_group_by_id(groupid: str):
    group = mongo.db.curso.find_one(ObjectId(groupid))
    if not group:
        raise HTTPException('Grupo no encontrado')
    return group

def get_groups():
    return mongo.db.curso.find()

def verify_if_group_exists(group_name: str):
    return mongo.db.curso.find_one({'name': group_name})

def update_group(groupid: str, data: dict):
    groupid = ObjectId(groupid)
    group = mongo.db.curso.find_one(groupid)
    if not group:
        raise HTTPException('Grupo no encontrado')
    
    if group['name'] != data['name'] and verify_if_group_exists(data['name']):
        raise HTTPException('El grupo ya existe')
    
    data['updated_at'] = datetime.now()
    updated = mongo.db.curso.update_one({'_id': groupid}, {'$set': data})
    if not updated:
        raise HTTPException('Grupo no encontrado')
    return updated

