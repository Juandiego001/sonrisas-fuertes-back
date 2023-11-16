from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId
from app.services.profile_user import create_user_profile


def verify_if_admin_exists(params: list):
    return mongo.db.users.find_one({'$or': params})


def create_admin(params: dict):
    verify_params = [{key:value for key, value in params.items()
                      if key in ['username', 'email', 'document']}]
    admin = verify_if_admin_exists(verify_params)
    if admin:
        raise HTTPException('El usuario ya existe')
    params['status'] = 'PENDING'
    params['updated_at'] = datetime.now()
    profileid = mongo.db.profiles.find_one({'name': 'Administrador'})['_id']
    adminid = mongo.db.users.insert_one(params).inserted_id
    return create_user_profile({
        'userid': adminid,
        'profileid': profileid
    })


def get_admin_by_id(adminid: str):
    admin = mongo.db.users.find_one(ObjectId(adminid))
    if not admin:
        raise HTTPException('Administrador no encontrado')
    return admin


def get_admins():
    return list(mongo.db.user_profiles.aggregate([
        {
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
                'profile.name': 'Administrador'
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


def update_admin(adminid, params):
    adminid = ObjectId(adminid)
    admin = mongo.db.users.find_one(adminid)
    if not admin:
        raise HTTPException('Administrador no encontrado')
    
    verify_data = [
        {'username': params['username']\
         if admin['username'] != params['username'] else ''},
        {'email': params['email']\
         if admin['email'] != params['email'] else ''},
        {'document': params['document']\
         if admin['document'] != params['document'] else ''}
    ]

    if verify_if_admin_exists(verify_data):
        raise HTTPException('El usuario ya existe')
    
    params['updated_at'] = datetime.now()

    # Se evita que al actualizar se reinicie la contraseña de manera
    # no deseada
    if params['password'] == '':
        params.pop('password')

    updated = mongo.db.users.update_one({'_id': adminid}, {'$set': params})
    if not updated:
        raise HTTPException('Administrador no encontrado')
    return updated

