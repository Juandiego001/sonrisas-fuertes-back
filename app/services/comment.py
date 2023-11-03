from datetime import datetime
from app import mongo
from app.services import publication
from bson import ObjectId
from werkzeug.exceptions import HTTPException
from app.services import file as fileService
from app.services import link as linkService


def save_comment_files(commentid: str, files: list):
    for file in files:
        fileService.put_file({'commentid': ObjectId(commentid), 'file': file})


def save_comment_links(commentid: str, param_links: list):
    links = []
    for link in param_links:
        link['commentid'] = ObjectId(commentid)
        link['created_at'] = link['updated_at'] = datetime.now()
        link['status'] = True
        links.append(link)
    linkService.create_multiple_links(links)


def create_comment(params: dict):
    if not publication.verify_publication_exists(params['publicationid']):
        raise HTTPException('Publicación no encontrada')
    params['userid'] = ObjectId(params['userid'])
    params['created_at'] = datetime.now()
    params['updated_at'] = datetime.now()
    params['status'] = True
    files = params.pop('files') if 'files' in params else []
    links = params.pop('links') if 'links' in params else []

    commentid = mongo.db.comments.insert_one(params).inserted_id
    if not commentid:
        raise HTTPException('El comentario no fue creado')
    if len(files):
        save_comment_files(commentid, files)
    if len(links):
        save_comment_links(commentid, links)
    return commentid


def get_comments():
    return list(mongo.db.comments.find({}))


def get_comment(commentid: str):
    return mongo.db.comments.aggregate([
        {
          '$lookup': {
            'from': 'links',
            'localField': '_id',
            'foreignField': 'commentid',
            'as': 'links'
          }
        },
        {
          '$lookup': {
            'from': 'files',
            'localField': '_id',
            'foreignField': 'commentid',
            'as': 'files'
          }
        },
        {
          '$match': {
            '$expr': {
              '$eq': [
                '$_id', ObjectId(commentid)]
            }
          }
        },
        {
          '$project': {
            '_id': 1,
            'description': 1,
            'updated_at': 1,
            'updated_by': 1,
            'created_at': 1,
            'files': 1,
            'links': 1
          }
        }
    ]).next()


def verify_comment_exists(commentid: str):
    return mongo.db.comments.find_one(ObjectId(commentid))


def get_comment_by_id(commentid: str):
    comment = verify_comment_exists(commentid)
    if not comment:
        raise HTTPException('Comentario no encontrado')
    return get_comment(commentid)


def delete_comment_attachments(commentid: str):
    files = list(mongo.db.files.find(
        {'commentid': ObjectId(commentid)}))
    for file in files:
        fileService.delete_file(file['_id'])
    links = mongo.db.links.find({'commentid': ObjectId(commentid)})
    for link in links:
        linkService.delete_link(link['_id'])


def update_comment(commentid: str, params: dict):
    if not verify_comment_exists(commentid):
        raise HTTPException('Comentario no encontrado')
    if 'status' in params and params['status'] == False:
        delete_comment_attachments(commentid)
    else:
        files = params.pop('files') if 'files' in params else []
        links = params.pop('links') if 'links' in params else []
        if len(files):
            save_comment_files(commentid, files)
        if len(links):
            save_comment_links(commentid, links)

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