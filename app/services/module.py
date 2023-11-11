from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId
from datetime import datetime


def verify_module_exists(params: dict):
  return mongo.db.modules.find_one(params)


def create_module(params: dict):
  if verify_module_exists({'name': params['name']}):
    raise HTTPException('El módulo ya existe')
  params['updated_at'] = datetime.now()
  params['status'] = True
  created = mongo.db.modules.insert_one(params)
  if not created:
    raise HTTPException('El módulo no ha sido creado')
  return created


def get_module(moduleid: str):
  return mongo.db.modules.find_one(ObjectId(moduleid))


def get_modules():
  return mongo.db.modules.find({})


def get_module_by_id(moduleid: str):
  module = verify_module_exists({'_id': ObjectId(moduleid)})
  if not module:
    raise HTTPException('Módulo no encontrado')
  return module


def update_module(moduleid: str, params: dict):
  module = verify_module_exists({'_id': ObjectId(moduleid)})
  if not module:
    raise HTTPException('Módulo no encontrado')
  
  if 'name' in params and module['name'] != params['name'] and\
    verify_module_exists({'name': params['name']}):
    raise HTTPException('El módulo ya existe')

  updated = mongo.db.modules.update_one({'_id': ObjectId(moduleid)}, 
                              {'$set': params})
  
  if not updated:
    raise HTTPException('El módulo no fue actualizado')
  return updated



