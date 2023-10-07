from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId
from app.services.profile_user import create_profile_user

def create_admin(params: dict):
    admin = verify_if_admin_exists([
        {'username': params['username']},
        {'email': params['email']},
        {'document': params['document']},
    ])
    if admin:
        raise HTTPException('El usuario ya existe')
    params['status'] = 'PENDING'
    params['updated_at'] = datetime.now()
    profileid = mongo.db.perfil.find_one({'name': 'Administrador'})['_id']
    adminid = mongo.db.usuario.insert_one(params).inserted_id
    return create_profile_user({
        'userid': adminid,
        'profileid': profileid
    })    

def get_admin_by_id(adminid: str):
    admin = mongo.db.usuario.find_one(ObjectId(adminid))
    if not admin:
        raise HTTPException('Admin not found')
    return admin

def get_admins():
    return list(mongo.db.perfil_usuario.aggregate(
        [{
            '$lookup': {
                'from': 'perfil', 
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
                'from': 'usuario', 
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

def verify_if_admin_exists(data: list):
    return mongo.db.usuario.find_one({'$or': data})

def update_admin(adminid, data):
    adminid = ObjectId(adminid)
    admin = mongo.db.usuario.find_one({'_id': adminid})
    if not admin:
        raise HTTPException('Admin was not found')
    
    verify_data = [
        {'username': data['username']\
         if admin['username'] != data['username'] else ''},
        {'email': data['email']\
         if admin['email'] != data['email'] else ''},
        {'document': data['document']\
         if admin['document'] != data['document'] else ''}
    ]

    if verify_if_admin_exists(verify_data):
        raise HTTPException('User already registered')
    
    data['updated_at'] = datetime.now()

    # Se evita que al actualizar se reinicie la contraseña de manera
    # no deseada
    if data['password'] == '':
        data.pop('password')

    updated = mongo.db.usuario.update_one({'_id': adminid}, {'$set': data})

    if not updated:
        raise HTTPException('User not found')
    return admin

