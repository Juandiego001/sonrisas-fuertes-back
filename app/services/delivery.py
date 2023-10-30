from datetime import datetime
import hashlib
from app import mongo, dbx
from app.services import activity
from bson import ObjectId
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from app.utils import generate_id


def upload_delivery_file(deliveryid, file, updated_by):
    filename = secure_filename(file.filename)
    format = filename.split('.')[-1]
    hash_name = (f'{hashlib.sha1(generate_id().encode("utf-8")).hexdigest()}.'
                 f'{format}')
    dbx.files_upload(file.read(), f'/deliveries/{deliveryid}/{hash_name}')
    url = f'{hash_name}?v={generate_id()}'
    return mongo.db.attachments.insert_one({
        'deliveryid': ObjectId(deliveryid),
        'folderid': None,
        'activityid': None,
        'hash_name': hash_name,
        'real_name': filename,
        'url': url,
        'status': True,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'updated_by': updated_by
    })


def create_delivery(params: dict):
    if not activity.verify_activity_exists(params['activityid']):
        raise HTTPException('Actividad no encontrada')
    
    params['userid'] = ObjectId(params['userid'])
    params['created_at'] = datetime.now()
    params['updated_at'] = datetime.now()
    params['status'] = True

    files = []
    if 'files' in params:
        files = params.pop('files')

    links = []
    if 'links' in params:
        links = params.pop('links')

    deliveryid = mongo.db.deliveries.insert_one(params).inserted_id

    if len(files):
        for file in files:
            upload_delivery_file(deliveryid, file, params['updated_by'])
    
    if len(links):
        mongo.db.attachments.insert_many([{
            'deliveryid': ObjectId(deliveryid),
            'folderid': None,
            'activityid': None,
            'hash_name': None,
            'real_name': None,
            'url': link,
            'isLink': True,
            'status': True,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'updated_by': params['updated_by']
        } for link in links])

    return deliveryid


def get_deliveries():
    return mongo.db.deliveries.find({})


def verify_delivery_exists(activityid: str):
    return mongo.db.deliveries.find_one(ObjectId(activityid))


def get_delivery_by_id(deliveryid: str):
    delivery = verify_delivery_exists(deliveryid)
    if not delivery:
        raise HTTPException('Entrega no encontrada')
    return delivery


def update_delivery(deliveryid: str, params: dict):
    if not verify_delivery_exists(deliveryid):
        raise HTTPException('Entrega no encontrada')
    params['updated_at'] = datetime.now()
    updated = mongo.db.deliveries.update_one(
        {'_id': ObjectId(deliveryid)}, {'$set': params})
    if not updated:
        raise HTTPException('La entrega no fue actualizada')
    return updated


def delete_delivery(deliveryid: str):
    if not verify_delivery_exists(deliveryid):
        raise HTTPException('Entrega no encontrada')
    deleted = mongo.db.deliveries.delete_one(ObjectId(deliveryid))
    if not deleted:
        raise HTTPException('La entrega no fue eliminada')
    return deleted