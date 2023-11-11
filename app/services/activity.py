from datetime import datetime
from app import mongo
from bson import ObjectId
from werkzeug.exceptions import HTTPException
from app.services import file as fileService
from app.services import link as linkService


def save_activity_files(activityid: str, files: list):
    for file in files:
        fileService.put_file({'activityid': ObjectId(activityid), 'file': file})


def save_activity_links(activityid: str, param_links: list):
    links = []
    for link in param_links:
        link['activityid'] = ObjectId(activityid)
        link['created_at'] = link['updated_at'] = datetime.now()
        link['status'] = True
        links.append(link)
    linkService.create_multiple_links(links)


def create_activity(params: dict):
    params['userid'] = ObjectId(params['userid'])
    params['updated_at'] = datetime.now()
    params['created_at'] = datetime.now()
    params['status'] = True
    files = params.pop('files') if 'files' in params else []
    links = params.pop('links') if 'links' in params else []

    activityid = mongo.db.activities.insert_one(params).inserted_id
    if not activityid:
        raise HTTPException('La actividad no fue creada')
    if len(files):
        save_activity_files(activityid, files)
    if len(links):
        save_activity_links(activityid, links)
    return activityid


def get_activities():
    return mongo.db.activities.aggregate([
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
            'foreignField': 'activityid', 
            'as': 'links'
        }
    }, {
        '$lookup': {
            'from': 'files', 
            'localField': '_id', 
            'foreignField': 'activityid', 
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


def get_activity_delivery(activityid: str, username: str):
    return mongo.db.activities.aggregate([
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
                'foreignField': 'activityid', 
                'as': 'links'
            }
        }, {
            '$lookup': {
                'from': 'files', 
                'localField': '_id', 
                'foreignField': 'activityid', 
                'as': 'files'
            }
        }, {
          '$lookup': {
            'from': 'deliveries',
            'localField': '_id',
            'foreignField': 'activityid',
            'let': {
                'delivery_status': '$status'
            },
            'pipeline': [
              {
                '$lookup': {
                  'from': 'users',
                  'localField': 'userid',
                  'foreignField': '_id',
                  'as': 'user_delivery'
                }
              },
              {
                 '$lookup': {
                  'from': 'links',
                  'localField': '_id',
                  'foreignField': 'deliveryid',
                  'as': 'links'
                } 
              },
              {
                '$lookup': {
                  'from': 'files',
                  'localField': '_id',
                  'foreignField': 'deliveryid',
                  'as': 'files'
                }   
              },
              {
                '$unwind': {
                  'path': '$user_delivery'
                }
              },
              {
                '$match': {
                    '$expr': {
                        '$and': [
                            {
                                '$eq': [
                                    '$$delivery_status', True
                                ]
                            },
                            {
                                '$eq': [
                                    '$user_delivery.username', username
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
                  'username': '$user_delivery.username',
                  'links': 1,
                  'files': 1,
                  'fullname': {"$concat": ["$user_delivery.name", " ", "$user_delivery.lastname"]}
                }
              },
              {
                  '$sort': {
                      'created_at': -1
                  }
              }
              ],
            'as': 'delivery'
          }
        }, {
            '$unwind': {
                'path': '$delivery',
                'preserveNullAndEmptyArrays': True
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
                'delivery': 1,
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


def get_activity_deliveries(activityid: str):
    return mongo.db.activities.aggregate([
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
                'foreignField': 'activityid', 
                'as': 'links'
            }
        }, {
            '$lookup': {
                'from': 'files', 
                'localField': '_id', 
                'foreignField': 'activityid', 
                'as': 'files'
            }
        }, {
          '$lookup': {
            'from': 'deliveries',
            'localField': '_id',
            'foreignField': 'activityid',
            'pipeline': [
              {
                '$lookup': {
                  'from': 'users',
                  'localField': 'userid',
                  'foreignField': '_id',
                  'as': 'user_delivery'
                }
              },
              {
                 '$lookup': {
                  'from': 'links',
                  'localField': '_id',
                  'foreignField': 'deliveryid',
                  'as': 'links'
                } 
              },
              {
                '$lookup': {
                  'from': 'files',
                  'localField': '_id',
                  'foreignField': 'deliveryid',
                  'as': 'files'
                }   
              },
              {
                '$unwind': {
                  'path': '$user_delivery'
                }
              },
              {
                '$project': {
                  '_id': 1,
                  'description': 1,
                  'status': 1,
                  'created_at': 1,
                  'username': '$user_delivery.username',
                  'links': 1,
                  'files': 1,
                  'fullname': {"$concat": ["$user_delivery.name", " ", "$user_delivery.lastname"]}
                }
              },
              {
                  '$sort': {
                      'created_at': -1
                  }
              }
              ],
            'as': 'deliveries'
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
                'deliveries': 1,
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


def get_activity(activityid: str):
    return mongo.db.activities.aggregate([
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
                'foreignField': 'activityid', 
                'as': 'links'
            }
        }, {
            '$lookup': {
                'from': 'files', 
                'localField': '_id', 
                'foreignField': 'activityid', 
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
                'deliveries': 1,
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


def verify_activity_exists(activityid: str):
    return mongo.db.activities.find_one(ObjectId(activityid))


def get_activity_by_id_delivery(activityid: str, username: str):
    activity = verify_activity_exists(activityid)
    if not activity:
        raise HTTPException('Actividad no encontrada')
    return get_activity_delivery(activityid, username)


def get_activity_by_id_deliveries(activityid: str):
    activity = verify_activity_exists(activityid)
    if not activity:
        raise HTTPException('Actividad no encontrada')
    return get_activity_deliveries(activityid)


def get_activity_by_id(activityid: str):
    activity = verify_activity_exists(activityid)
    if not activity:
        raise HTTPException('Actividad no encontrada')
    return get_activity(activityid)


def delete_activity_attachments(activityid: str):
    files = list(mongo.db.files.find({'activityid': ObjectId(activityid)}))
    for file in files:
        fileService.delete_file(file['_id'])
    links = mongo.db.links.find({'activityid': ObjectId(activityid)})
    for link in links:
        linkService.delete_link(link['_id'])


def update_activity(activityid: str, params: dict):
    if not verify_activity_exists(activityid):
        raise HTTPException('Actividad no encontrada')
    if 'status' in params and params['status'] == False:
        delete_activity_attachments(activityid)
    else:
        files = params.pop('files') if 'files' in params else []
        links = params.pop('links') if 'links' in params else []
        if len(files):
            save_activity_files(activityid, files)
        if len(links):
            save_activity_links(activityid, links)

    params['updated_at'] = datetime.now()
    updated = mongo.db.activities.update_one(
        {'_id': ObjectId(activityid)}, {'$set': params})
    if not updated:
        raise HTTPException('La actividad no ha sido actualizada')
    return updated