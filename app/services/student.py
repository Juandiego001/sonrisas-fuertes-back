from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId
from app.services.profile_user import create_user_profile


def verify_if_student_exists(params: list):
    return mongo.db.users.find_one({'$or': params})


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
    profileid = mongo.db.profiles.find_one({'name': 'Estudiante'})['_id']
    studentid = mongo.db.users.insert_one(params).inserted_id
    return create_user_profile({
        'userid': studentid,
        'profileid': profileid
    })
        

def get_student_by_id(studentid: str):
    student = mongo.db.users.find_one(ObjectId(studentid))
    if not student:
        raise HTTPException('Estudiante no encontrado')
    return student


def get_students(query: dict = {}):
    return list(mongo.db.perfil_usuario.aggregate(
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


def update_student(studentid, params):
    studentid = ObjectId(studentid)
    student = mongo.db.users.find_one({'_id': studentid})
    if not student:
        raise HTTPException('Estudiante no encontrado')

    verify_data = [
        {'username': params['username']\
         if student['username'] != params['username'] else ''},
        {'email': params['email']\
         if student['email'] != params['email'] else ''},
        {'document': params['document']\
         if student['document'] != params['document'] else ''}
    ]

    if verify_if_student_exists(verify_data):
        raise HTTPException('El usuario ya existe')
    
    params['updated_at'] = datetime.now()

    # Se evita que al actualizar se reinicie la contraseña de manera
    # no deseada
    if params['password'] == '':
        params.pop('password')

    updated = mongo.db.users.update_one({'_id': studentid}, {'$set': params})
    if not updated:
        raise HTTPException('El estudiante no fue actualizado')
    return updated
