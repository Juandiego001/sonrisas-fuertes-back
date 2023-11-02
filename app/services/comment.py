from datetime import datetime
import hashlib
from app import mongo, dbx
from app.services import publication
from bson import ObjectId
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from app.utils import generate_id


def upload_comment_file(commentid, file, updated_by):
    filename = secure_filename(file.filename)
    format = filename.split('.')[-1]
    hash_name = (f'{hashlib.sha1(generate_id().encode("utf-8")).hexdigest()}.'
                 f'{format}')
    dbx.files_upload(file.read(), f'/comments/{commentid}/{hash_name}')
    url = f'{hash_name}?v={generate_id()}'
    return mongo.db.attachments.insert_one({
        'commentid': ObjectId(commentid),
        'folderid': None,
        'publicationid': None,
        'hash_name': hash_name,
        'real_name': filename,
        'url': url,
        'status': True,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'updated_by': updated_by
    })


def create_comment(params: dict):
    if not publication.verify_publication_exists(params['publicationid']):
        raise HTTPException('Publicación no encontrada')
    
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

    commentid = mongo.db.comments.insert_one(params).inserted_id

    if len(files):
        for file in files:
            upload_comment_file(commentid, file, params['updated_by'])
    
    if len(links):
        mongo.db.attachments.insert_many([{
            'commentid': ObjectId(commentid),
            'folderid': None,
            'publicationid': None,
            'hash_name': None,
            'real_name': None,
            'url': link,
            'isLink': True,
            'status': True,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'updated_by': params['updated_by']
        } for link in links])

    return commentid


def get_comments():
    return mongo.db.comments.find({})


def verify_comment_exists(publicationid: str):
    return mongo.db.comments.find_one(ObjectId(publicationid))


def get_comment_by_id(commentid: str):
    comment = verify_comment_exists(commentid)
    if not comment:
        raise HTTPException('Comentario no encontrado')
    return comment


def update_comment(commentid: str, params: dict):
    if not verify_comment_exists(commentid):
        raise HTTPException('Comentario no encontrado')
    
    params['updated_at'] = datetime.now()
    updated = mongo.db.comments.update_one(
        {'_id': ObjectId(commentid)}, {'$set': params})
    if not updated:
        raise HTTPException('El comentario no fue actualizado')
    
    return updated


def delete_comment(commentid: str):
    if not verify_comment_exists(commentid):
        raise HTTPException('Comentario no encontrado')
    
    deleted = mongo.db.comments.delete_one(ObjectId(commentid))
    if not deleted:
        raise HTTPException('El comentario no fue eliminado')
    return deleted