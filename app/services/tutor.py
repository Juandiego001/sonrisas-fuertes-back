from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId
from app.services.profile_user import create_user_profile


def verify_if_tutor_exists(params: list):
    return mongo.db.users.find_one({'$or': params})


def create_tutor(params: dict):
    verify_params = [{key:value for key, value in params.items()
                      if key in ['username', 'email', 'document']}]
    tutor = verify_if_tutor_exists(verify_params)
    if tutor:
        raise HTTPException('El usuario ya existe')
    params['status'] = 'PENDING'
    params['updated_at'] = datetime.now()
    profileid = mongo.db.profiles.find_one({'name': 'Acudiente'})['_id']
    tutorid = mongo.db.users.insert_one(params).inserted_id
    return create_user_profile({
        'userid': tutorid,
        'profileid': profileid
    })    


def get_tutor_by_id(tutorid: str):
    tutor = mongo.db.users.find_one(ObjectId(tutorid))
    if not tutor:
        raise HTTPException('Acudiente no encontrado')
    return tutor


def get_tutors():
    return list(mongo.db.user_profiles.aggregate(
        [{
            '$lookup': {
                'from': 'profiles', 
                'localField': 'profileid', 
                'foreignField': '_id', 
                'as': 'profile'
            }
        }, {
            '$unwind': {
                'path': '$profile'
            }
        }, {
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
                'profile.name': 'Acudiente'
            },
        }, {
            '$project': {
                '_id': '$user._id',
                'name': '$user.name',
                'lastname': '$user.lastname',
                'document': '$user.document',
                'username': '$user.username',
                'email': '$user.email',
                'kinship': '$user.kinship',
                'phone': '$user.phone',
                'regime': '$user.regime',
                'status': '$user.status',
                'updated_by': '$user.updated_by',
                'updated_at': '$user.updated_at',
            }
        }]))


def update_tutor(tutorid, params):
    tutorid = ObjectId(tutorid)
    tutor = mongo.db.users.find_one(tutorid)
    if not tutor:
        raise HTTPException('Acudiente no encontrado')
    
    verify_data = [
        {'username': params['username']\
         if tutor['username'] != params['username'] else ''},
        {'email': params['email']\
         if tutor['email'] != params['email'] else ''},
        {'document': params['document']\
         if tutor['document'] != params['document'] else ''}
    ]

    if verify_if_tutor_exists(verify_data):
        raise HTTPException('El usuario ya existe')
    
    params['updated_at'] = datetime.now()

    # Se evita que al actualizar se reinicie la contraseña de manera
    # no deseada
    if params['password'] == '':
        params.pop('password')

    updated = mongo.db.users.update_one({'_id': tutorid}, {'$set': params})

    if not updated:
        raise HTTPException('Acudiente no encontrado')
    return updated

