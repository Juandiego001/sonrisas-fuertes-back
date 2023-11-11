from http.client import HTTPException
from app import mongo
from bson import ObjectId


def verify_profile_exists(profileid: str):
    return mongo.db.profiles.find_one(ObjectId(profileid))


def create_profile(params: dict):
    return mongo.db.profiles.insert_one(params)


def get_profile(profileid: str):
    return mongo.db.profiles.aggregate([
        {
            '$lookup': {
                'from': 'permissions',
                'localField': '_id',
                'foreignField': 'profileid',
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'modules',
                            'localField': 'moduleid',
                            'foreignField': '_id',
                            'as': 'module'
                        }
                    }, {
                        '$unwind': {
                            'path': '$module'
                        }
                    }, {
                        '$project': {
                            'read': 1,
                            'create': 1,
                            'update': 1,
                            'delete': 1,
                            'module': '$module.name'
                        }
                    }
                ],
                'as': 'permissions'
            }
        }, {
            '$match': {
                '$expr': {
                    '$eq': [
                        '$_id', ObjectId(profileid)
                    ]
                }
            }
        }, {
            '$project': {
                'name': 1,
                'status': 1,
                'permissions': '$permissions'
            }
        }
    ]).try_next()


def get_profiles():
    return list(mongo.db.profiles.find())


def get_profile_detail(profileid: str):
    profile = mongo.db.profiles.find_one(ObjectId(profileid))
    if not profile:
        raise HTTPException('Perfil no encontrado')
    return get_profile(profileid)


def update_profile(profileid: str, profile: dict):
    profile = mongo.db.profiles.find_one_and_update(
        {'_id': ObjectId(profileid)},
        {'$set': profile})
    if not profile:
        raise HTTPException('Perfil no encontrado')
    return profile