from datetime import datetime
from app import mongo
from app.services.publication import verify_publication_exists
from bson import ObjectId
from werkzeug.exceptions import HTTPException

def create_comment(params: dict):
    if not verify_publication_exists(params['publicationid']):
        raise HTTPException('Publicación no encontrada')
    params['userid'] = ObjectId(params['userid'])
    params['created_at'] = datetime.now()
    params['updated_at'] = datetime.now()
    params['status'] = True
    mongo.db.comments.insert_one(params)

def get_comments():
    return mongo.db.comments.find({})

def get_comment_by_id(commentid: str):
    comment = verify_comment_exists(commentid)
    if not comment:
        raise HTTPException('Comentario no encontrado')
    return mongo.db.comments.find_one({'_id': ObjectId(commentid)})

def verify_comment_exists(publicationid: str):
    return mongo.db.comments.find_one(ObjectId(publicationid))

def update_comment(commentid: str, params: dict):
    if not verify_comment_exists(commentid):
        raise HTTPException('Comentario no encontrado')
    
    params['updated_at'] = datetime.now()
    updated = mongo.db.comments.update_one(
        {'_id': ObjectId(commentid)}, {'$set': params})
    if not updated:
        raise HTTPException('El comentario no ha sido actualizado')
    
    return updated