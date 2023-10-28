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

def get_publications(isActivity=False):
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
                '$and': [
                    {
                        '$eq': [
                            '$status', True
                        ]
                    },
                    {
                        '$eq': [
                            '$isActivity', isActivity
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

def get_publication_user_comments(publicationid: str, username=''):
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
          '$lookup': {
            'from': 'comments',
            'localField': '_id',
            'foreignField': 'publicationid',
            'pipeline': [
              {
                '$lookup': {
                  'from': 'usuario',
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
    return get_publication_user_comments(publicationid)
    

def verify_publication_exists(publicationid: str, isActivity=False):
    return mongo.db.publicacion.find_one({'_id': ObjectId(publicationid), 
                                          'isActivity': isActivity})


def update_publication(publicationid: str, params: dict):
    if not verify_publication_exists(publicationid):
        raise HTTPException('Publicación no encontrada')
    
    params['updated_at'] = datetime.now()
    updated = mongo.db.publicacion.update_one(
        {'_id': ObjectId(publicationid)}, {'$set': params})
    if not updated:
        raise HTTPException('La publicación no ha sido actualizada')
    
    return updated


def get_activity(activityid: str, username: str):
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
          '$lookup': {
            'from': 'comments',
            'localField': '_id',
            'foreignField': 'publicationid',
            'pipeline': [
              {
                '$lookup': {
                  'from': 'usuario',
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
                        '$and': [
                            {
                                '$eq': [
                                    '$status', True
                                ]
                            },
                            {
                                '$eq': [
                                    '$user.username', username
                                ]
                            }
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
                                '$_id', ObjectId(activityid)
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


def get_activity_by_id(activityid: str, username: str):
    activity = verify_publication_exists(activityid, True)
    if not activity:
        raise HTTPException('Actividad no encontrada')
    return get_activity(activityid, username)