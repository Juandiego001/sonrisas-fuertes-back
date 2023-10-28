from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId
from app.services.profile_user import create_profile_user

def create_student(params: dict):
    student = verify_if_student_exists([
        {'username': params['username']},
        {'email': params['email']},
        {'document': params['document']},
    ])
    if student:
        raise HTTPException('El usuario ya existe')
    params['status'] = 'PENDING'
    params['updated_at'] = datetime.now()
    profileid = mongo.db.perfil.find_one({'name': 'Estudiante'})['_id']
    studentid = mongo.db.usuario.insert_one(params).inserted_id
    return create_profile_user({
        'userid': studentid,
        'profileid': profileid
    })
        

def get_student_by_id(studentid: str):
    student = mongo.db.usuario.find_one(ObjectId(studentid))
    if not student:
        raise HTTPException('Student not found')
    return student

def get_students(query: dict = {}):
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
                '$and': [
                    {'profile.name': 'Estudiante'},
                    query
                ]
            },
        }, {
            '$project': {
                '_id': '$user._id',
                'name': '$user.name',
                'lastname': '$user.lastname',
                'document': '$user.document',
                'username': '$user.username',
                'email': '$user.email',
                'age': '$user.age',
                'born_at': '$user.born_at',
                'diagnosis': '$user.diagnosis',
                'eps': '$user.eps',
                'gender': '$user.gender',
                'godfather': '$user.godfather',
                'observations': '$user.observations',
                'status': '$user.status',
                'updated_by': '$user.updated_by',
                'updated_at': '$user.updated_at',
            }
        }]))

def verify_if_student_exists(data: list):
    return mongo.db.usuario.find_one({'$or': data})

def update_student(studentid, data):
    studentid = ObjectId(studentid)
    student = mongo.db.usuario.find_one({'_id': studentid})
    if not student:
        raise HTTPException('Student was not found')

    verify_data = [
        {'username': data['username']\
         if student['username'] != data['username'] else ''},
        {'email': data['email']\
         if student['email'] != data['email'] else ''},
        {'document': data['document']\
         if student['document'] != data['document'] else ''}
    ]

    if verify_if_student_exists(verify_data):
        raise HTTPException('User already registered')
    
    data['updated_at'] = datetime.now()

    # Se evita que al actualizar se reinicie la contraseña de manera
    # no deseada
    if data['password'] == '':
        data.pop('password')

    updated = mongo.db.usuario.update_one({'_id': studentid}, {'$set': data})
    
    if not updated:
        raise HTTPException('User not found')
    return student

def get_students_by_group(groupid: str):
    return get_students(
        {'user.groupid': ObjectId(groupid) if groupid else None})