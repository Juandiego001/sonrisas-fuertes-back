from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId
from app.services.profile_user import create_profile_user

def create_teacher(params: dict):
    teacher = get_teacher_detail(params)
    if teacher:
        raise HTTPException('El usuario ya existe')
    params['updated_at'] = datetime.now()

    profileid = mongo.db.perfil.find_one({'name': 'Profesor'})['_id']
    teacherid = mongo.db.usuario.insert_one(params).inserted_id
    return create_profile_user({
        'userid': teacherid,
        'profileid': profileid
    })    

def get_teacher_by_id(teacherid: str):
    teacher = mongo.db.usuario.find_one(ObjectId(teacherid))
    if not teacher:
        raise HTTPException('Teacher not found')
    return teacher

def get_teacher_detail(params: dict):
    return mongo.db.usuario.find_one(
        {
            '$or': 
            [
                {'email': params['email']},
                {'username': params['username']},
                {'document': params['document']}
            ]
        })

def get_teachers():
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



def update_teacher(teacherid, data):
    teacher = mongo.db.usuario.find_one_and_update(
        {'_id': ObjectId(teacherid)},
        {'$set': data})
    if not teacher:
        raise HTTPException('Teacher was not found')
    return teacher

