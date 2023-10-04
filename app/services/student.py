from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId
from app.services.profile_user import create_profile_user

def create_student(params: dict):
    student = get_student_detail(params)
    if student:
        raise HTTPException('El usuario ya existe')
    params['updated_at'] = datetime.now()
    profileid = mongo.db.perfil.find_one({'name': 'estudiante'})['_id']
    studentid = mongo.db.usuario.insert_one(params).inserted_id
    return create_profile_user({
        'userid': studentid,
        'profileid': profileid,
        'status': True,
        'updated_by': params['updated_by'],
        'updated_at': params['updated_at']
    })
        

def get_student_by_id(studentid: str):
    student = mongo.db.usuario.find_one(ObjectId(studentid))
    if not student:
        raise HTTPException('Student not found')
    return student

def get_students():
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
                'profile_info.name': 'estudiante'
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

def get_student_detail(params: dict):
    return mongo.db.usuario.find_one(
        {
            '$or': 
            [
                {'email': params['email']},
                {'username': params['username']},
                {'document': params['document']}
            ]
        })

def update_student(studentid, data):
    student = mongo.db.usuario.find_one_and_update(
        {'_id': ObjectId(studentid)},
        {'$set': data})
    if not student:
        raise HTTPException('Student was not found')
    return student

