from datetime import datetime
from app import mongo
from bson import ObjectId
from werkzeug.exceptions import HTTPException


def create_publication(params: dict):
    params['userid'] = ObjectId(params['userid'])
    params['updated_at'] = datetime.now()
    params['created_at'] = datetime.now()
    params['status'] = True
    return mongo.db.publications.insert_one(params)


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
                  'from': 'attachments',
                  'localField': '_id',
                  'foreignField': 'commentid',
                  'as': 'attachments'
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


def update_publication(publicationid: str, params: dict):
    if not verify_publication_exists(publicationid):
        raise HTTPException('Publicación no encontrada')
    params['updated_at'] = datetime.now()
    updated = mongo.db.publications.update_one(
        {'_id': ObjectId(publicationid)}, {'$set': params})
    if not updated:
        raise HTTPException('La publicación no fue actualizada')
    return updated
