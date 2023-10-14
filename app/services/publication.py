from datetime import datetime
from app import mongo
from bson import ObjectId
from werkzeug.exceptions import HTTPException

def create_publication(params: dict):
    params['userid'] = ObjectId(params['userid'])
    params['updated_at'] = datetime.now()
    params['created_at'] = datetime.now()
    params['status'] = True
    return mongo.db.publicacion.insert_one(params)

def get_publications():
    return mongo.db.publicacion.aggregate([
    {
        '$lookup': {
            'from': 'usuario', 
            'localField': 'userid', 
            'foreignField': '_id', 
            'as': 'users'
        }
    }, {
        '$unwind': {
            'path': '$users'
        }
    }, {
        '$match': {
            '$expr': {
                '$eq': [
                    '$status', True
                ]
            }
        }
    }, {
        '$project': {
            '_id': 1,
            'description': 1,
            'created_at': 1,
            'status': 1,
            'username': "$users.username",
            'fullname': {"$concat": ["$users.name", " ", "$users.lastname"]}
        }
    },
    {
        '$sort': {
            'created_at': -1
        }
    }
])

def get_publication_by_id(publicationid: str):
    publication = verify_publication_exists(publicationid)
    if not publication:
        raise HTTPException('Publicación no encontrada')
    return publication
    

def verify_publication_exists(publicationid: str):
    return mongo.db.publicacion.find_one(ObjectId(publicationid))

def update_publication(publicationid: str, params: dict):
    if not verify_publication_exists(publicationid):
        raise HTTPException('Publicación no encontrada')
    
    params['updated_at'] = datetime.now()
    updated = mongo.db.publicacion.update_one(
        {'_id': ObjectId(publicationid)}, {'$set': params})
    if not updated:
        raise HTTPException('La publicación no ha sido actualizada')
    
    return updated