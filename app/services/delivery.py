from datetime import datetime
import hashlib
from app import mongo, dbx
from app.services import activity
from bson import ObjectId
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from app.services import file as fileService
from app.services import link as linkService
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


def save_delivery_files(deliveryid: str, files: list):
    for file in files:
        fileService.put_file({'deliveryid': ObjectId(deliveryid), 'file': file})


def save_delivery_links(deliveryid: str, param_links: list):
    links = []
    for link in param_links:
        link['deliveryid'] = ObjectId(deliveryid)
        link['created_at'] = link['updated_at'] = datetime.now()
        link['status'] = True
        links.append(link)
    linkService.create_multiple_links(links)


def create_delivery(params: dict):
    if not activity.verify_activity_exists(params['activityid']):
        raise HTTPException('Actividad no encontrada')
    
    params['userid'] = ObjectId(params['userid'])
    params['created_at'] = datetime.now()
    params['updated_at'] = datetime.now()
    params['status'] = True
    files = params.pop('files') if 'files' in params else []
    links = params.pop('links') if 'links' in params else []

    deliveryid = mongo.db.deliveries.insert_one(params).inserted_id
    if not deliveryid:
        raise HTTPException('La entrega no fue creada')
    if len(files):
        save_delivery_files(deliveryid, files)
    if len(links):
        save_delivery_links(deliveryid, links)
    return deliveryid


def get_deliveries():
    return mongo.db.deliveries.find({})


def get_delivery(deliveryid: str):
    return mongo.db.deliveries.aggregate([
        {
            '$lookup': {
                'from': 'users',
                'localField': 'userid',
                'foreignField': '_id',
                'as': 'user'
            }
        }, {
            '$unwind': {
                'path': '$user'
            }
        }, {
            '$lookup': {
                'from': 'links', 
                'localField': '_id', 
                'foreignField': 'deliveryid', 
                'as': 'links'
            }
        }, {
            '$lookup': {
                'from': 'files', 
                'localField': '_id', 
                'foreignField': 'deliveryid', 
                'as': 'files'
            }
        }, {
            '$match': {
                '$expr': {
                    '$and': [
                        {
                            '$eq': [
                                '$status', True
                            ]
                        },
                        {
                            '$eq': [
                                '$_id', ObjectId(deliveryid)
                            ]
                        }
                    ]
                }
            }
        }, {
            '$project': {
                '_id': 1,
                'title': 1,
                'description': 1,
                'created_at': 1,
                'status': 1,
                'username': "$user.username",
                'links': 1,
                'files': 1,
                'fullname': {"$concat": ["$user.name", " ", "$user.lastname"]}
            }
        },
        {
            '$sort': {
                'created_at': -1
            }
        }
    ]).try_next()


def verify_delivery_exists(paramid: str):
    return mongo.db.deliveries.find_one(ObjectId(paramid))


def get_delivery_by_id(deliveryid: str):
    delivery = verify_delivery_exists(deliveryid)
    if not delivery:
        raise HTTPException('Entrega no encontrada')
    return get_delivery(deliveryid)


def delete_delivery_attachments(deliveryid: str):
    files = list(mongo.db.files.find(
        {'deliveryid': ObjectId(deliveryid)}))
    for file in files:
        fileService.delete_file(file['_id'])
    links = mongo.db.links.find({'deliveryid': ObjectId(deliveryid)})
    for link in links:
        linkService.delete_link(link['_id'])


def update_delivery(deliveryid: str, params: dict):
    if not verify_delivery_exists(deliveryid):
        raise HTTPException('Entrega no encontrada')
    if 'status' in params and params['status'] == False:
        delete_delivery_attachments(deliveryid)
    else:
        files = params.pop('files') if 'files' in params else []
        links = params.pop('links') if 'links' in params else []
        if len(files):
            save_delivery_files(deliveryid, files)
        if len(links):
            save_delivery_links(deliveryid, links)


    params['updated_at'] = datetime.now()
    updated = mongo.db.deliveries.update_one(
        {'_id': ObjectId(deliveryid)}, {'$set': params})
    if not updated:
        raise HTTPException('La entrega no fue actualizada')
    return updated


def delete_delivery(deliveryid: str):
    if not verify_delivery_exists(deliveryid):
        raise HTTPException('Entrega no encontrada')
    deleted = mongo.db.deliveries.delete_one({'_id': ObjectId(deliveryid)})
    if not deleted:
        raise HTTPException('La entrega no fue eliminada')
    return deleted