from datetime import datetime
from app import mongo
from bson import ObjectId
from werkzeug.exceptions import HTTPException
from app.services import file as fileService
from app.services import link as linkService


def save_publication_files(publicationid: str, files: list):
    for file in files:
        fileService.put_file({'publicationid': ObjectId(publicationid), 'file': file})


def save_publication_links(publicationid: str, param_links: list):
    links = []
    for link in param_links:
        link['publicationid'] = ObjectId(publicationid)
        link['created_at'] = link['updated_at'] = datetime.now()
        link['status'] = True
        links.append(link)
    linkService.create_multiple_links(links)


def create_publication(params: dict):
    params['userid'] = ObjectId(params['userid'])
    params['updated_at'] = datetime.now()
    params['created_at'] = datetime.now()
    params['status'] = True
    files = params.pop('files') if 'files' in params else []
    links = params.pop('links') if 'links' in params else []

    publicationid = mongo.db.publications.insert_one(params).inserted_id
    if not publicationid:
        raise HTTPException('La publicación no fue creada')
    if len(files):
        save_publication_files(publicationid, files)
    if len(links):
        save_publication_links(publicationid, links)
    return publicationid


def get_publications():
    return mongo.db.publications.aggregate([
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
            'foreignField': 'publicationid', 
            'as': 'links'
        }
    }, {
        '$lookup': {
            'from': 'files', 
            'localField': '_id', 
            'foreignField': 'publicationid', 
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
])


def get_publication(publicationid: str):
    return mongo.db.publications.aggregate([
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
                'foreignField': 'publicationid', 
                'as': 'links'
            }
        }, {
            '$lookup': {
                'from': 'files', 
                'localField': '_id', 
                'foreignField': 'publicationid', 
                'as': 'files'
            }
        }, {
          '$lookup': {
            'from': 'comments',
            'localField': '_id',
            'foreignField': 'publicationid',
            'pipeline': [
              {
                '$lookup': {
                  'from': 'users',
                  'localField': 'userid',
                  'foreignField': '_id',
                  'as': 'user'
                }
              },
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
                '$unwind': {
                  'path': '$user'
                }
              },
              {
                '$match': {
                    '$expr': {    
                        '$eq': [
                            '$status', True
                        ]
                    }
                }
              },
              {
                '$project': {
                  '_id': 1,
                  'description': 1,
                  'status': 1,
                  'created_at': 1,
                  'attachments': 1,
                  'username': '$user.username',
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
              ],
            'as': 'comments'
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
                                '$_id', ObjectId(publicationid)
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
                'comments': 1,
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
    ])


def verify_publication_exists(publicationid: str):
    return mongo.db.publications.find_one(ObjectId(publicationid))


def get_publication_by_id(publicationid: str):
    publication = verify_publication_exists(publicationid)
    if not publication:
        raise HTTPException('Publicación no encontrada')
    return get_publication(publicationid)


def delete_publication_attachments(publicationid: str):
    files = list(mongo.db.files.find(
        {'publicationid': ObjectId(publicationid)}))
    for file in files:
        fileService.delete_file(file['_id'])
    links = mongo.db.links.find({'publicationid': ObjectId(publicationid)})
    for link in links:
        linkService.delete_link(link['_id'])


def update_publication(publicationid: str, params: dict):
    if not verify_publication_exists(publicationid):
        raise HTTPException('Publicación no encontrada')
    if 'status' in params and params['status'] == False:
        delete_publication_attachments(publicationid)
    else:
        files = params.pop('files') if 'files' in params else []
        links = params.pop('links') if 'links' in params else []
        if len(files):
            save_publication_files(publicationid, files)
        if len(links):
            save_publication_links(publicationid, links)

    params['updated_at'] = datetime.now()
    updated = mongo.db.publications.update_one(
        {'_id': ObjectId(publicationid)}, {'$set': params})
    if not updated:
        raise HTTPException('La publicación no fue actualizada')
    return updated
