from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId
from app.services.profile_user import create_user_profile


def verify_if_teacher_exists(params: list):
    return mongo.db.users.find_one({'$or': params})


def create_teacher(params: dict):
    verify_params = [{key:value for key, value in params.items()
                      if key in ['username', 'email', 'document']}]
    teacher = verify_if_teacher_exists(verify_params)
    if teacher:
        raise HTTPException('El usuario ya existe')
    params['status'] = 'PENDING'
    params['updated_at'] = datetime.now()
    profileid = mongo.db.profiles.find_one({'name': 'Profesor'})['_id']
    teacherid = mongo.db.users.insert_one(params).inserted_id
    return create_user_profile({
        'userid': teacherid,
        'profileid': profileid
    })    


def get_teacher_by_id(teacherid: str):
    teacher = mongo.db.users.find_one(ObjectId(teacherid))
    if not teacher:
        raise HTTPException('Profesor no encontrado')
    return teacher


def get_teachers():
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
                'profile.name': 'Profesor'
            },
        }, {
            '$project': {
                '_id': '$user._id',
                'name': '$user.name',
                'lastname': '$user.lastname',
                'document': '$user.document',
                'username': '$user.username',
                'email': '$user.email',
                'status': '$user.status',
                'updated_by': '$user.updated_by',
                'updated_at': '$user.updated_at',
            }
        }]))


def update_teacher(teacherid, params):
    teacherid = ObjectId(teacherid)
    teacher = mongo.db.users.find_one(teacherid)
    if not teacher:
        raise HTTPException('Profesor no encontrado')
    
    verify_data = [
        {'username': params['username']\
         if teacher['username'] != params['username'] else ''},
        {'email': params['email']\
         if teacher['email'] != params['email'] else ''},
        {'document': params['document']\
         if teacher['document'] != params['document'] else ''}
    ]

    if verify_if_teacher_exists(verify_data):
        raise HTTPException('El usuario ya existe')
    
    params['updated_at'] = datetime.now()

    # Se evita que al actualizar se reinicie la contraseña de manera
    # no deseada
    if params['password'] == '':
        params.pop('password')

    updated = mongo.db.users.update_one({'_id': teacherid}, {'$set': params})

    if not updated:
        raise HTTPException('Profesor no encontrado')
    return updated

