from app import mongo
from datetime import datetime
from bson import ObjectId
from werkzeug.exceptions import HTTPException

def verify_link_exists(linkid: str):
    return mongo.db.links.find_one(ObjectId(linkid))


def create_multiple_links(params: list):
    return mongo.db.links.insert_many(params)


def create_link(params: dict):
    params['created_at'] = params['updated_at'] = datetime.now()
    params['status'] = True
    return mongo.db.links.insert_one(params)


def get_links():
    return mongo.db.links.find({})


def get_link_detail(linkid):
    link = verify_link_exists(linkid)
    if not link:
        raise HTTPException('Enlace no encontrado')
    return link


def update_link(linkid: str, params: dict):
    link = verify_link_exists(linkid)
    if not link:
        raise HTTPException('Enlace no encontrado')
    params['updated_at'] = datetime.now()
    updated = mongo.db.links.update_one({'_id': ObjectId(linkid)},
                                        {'$set': params})
    if not updated:
        raise HTTPException('El enlace no fue actualizado')
    return updated


def delete_link(linkid: str):
    link = verify_link_exists(linkid)
    if not link:
        raise HTTPException('Enlace no encontrado')
    was_deleted = mongo.db.links.delete_one({'_id': ObjectId(linkid)})
    if not was_deleted:
        raise HTTPException('Enlace no eliminado de la base de datos')
    return was_deleted

    