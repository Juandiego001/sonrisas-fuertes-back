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
    profileid = mongo.db.perfil.find_one({'name': 'profesor'})['_id']
    teacherid = mongo.db.usuario.insert_one(params).inserted_id
    return create_profile_user({
        'userid': teacherid,
        'profileid': profileid,
        'status': True,
        'updated_by': params['updated_by'],
        'updated_at': params['updated_at']
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
                'as': 'profile_info'
            }
        }, {
            '$lookup': {
                'from': 'usuario', 
                'localField': 'userid', 
                'foreignField': '_id', 
                'as': 'user_info'
            }
        }, {
            '$unwind': {
                'path': '$user_info'
            }
        }, {
            '$match': {
                'profile_info.name': 'profesor'
            },
        }, {
            '$project': {
                '_id': '$user_info._id',
                'name': '$user_info.name',
                'lastname': '$user_info.lastname',
                'document': '$user_info.document',
                'username': '$user_info.username',
                'email': '$user_info.email',
                'status': '$user_info.status',
                'updated_by': '$user_info.updated_by',
                'updated_at': '$user_info.updated_at',
            }
        }]))



def update_teacher(teacherid, data):
    teacher = mongo.db.usuario.find_one_and_update(
        {'_id': ObjectId(teacherid)},
        {'$set': data})
    if not teacher:
        raise HTTPException('Teacher was not found')
    return teacher

