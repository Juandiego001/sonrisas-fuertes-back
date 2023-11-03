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

    tutorsid = params.pop('tutorsid') if 'tutorsid' in params else []
    studentid = mongo.db.users.insert_one(params).inserted_id

    if len(tutorsid):
        user_tutors = [{'tutorid': ObjectId(tutorid),
                        'userid': ObjectId(studentid)} for tutorid in tutorsid]
        mongo.db.user_tutors.insert_many(user_tutors)

    return create_user_profile({
        'userid': studentid,
        'profileid': profileid
    })
        

def get_student(studentid: str):
    return mongo.db.user_profiles.aggregate(
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
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'user_tutors',
                            'localField': '_id',
                            'foreignField': 'userid',
                            'pipeline': [
                                {
                                    '$lookup': {
                                        'from': 'users',
                                        'localField': 'tutorid',
                                        'foreignField': '_id',
                                        'as': 'tutors'
                                    },
                                },
                                {
                                    '$unwind': {
                                        'path': '$tutors'
                                    }
                                },
                                {
                                    '$project': {
                                        'tutorsid': {'$toString': '$tutors._id'}
                                    }
                                }
                            ],
                            'as': 'user_tutors'
                        }
                    }
                ],
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
                    {'user._id': ObjectId(studentid)}
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
                'hospital': '$user.hospital',
                'born_at': '$user.born_at',
                'diagnosis': '$user.diagnosis',
                'eps': '$user.eps',
                'gender': '$user.gender',
                'godfather': '$user.godfather',
                'city': '$user.city',
                'neighborhood': '$user.neighborhood',
                'address': '$user.address',
                'tutorsid': '$user.user_tutors.tutorsid',
                'observations': '$user.observations',
                'status': '$user.status',
                'updated_by': '$user.updated_by',
                'updated_at': '$user.updated_at',
            }
        }]).next()


def get_student_by_id(studentid: str):
    student = verify_if_student_exists([{'_id': ObjectId(studentid)}])
    if not student:
        raise HTTPException('Estudiante no encontrado')
    return get_student(studentid)


def get_students(query: dict = {}):
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
                'hospital': '$user.hospital',
                'born_at': '$user.born_at',
                'diagnosis': '$user.diagnosis',
                'eps': '$user.eps',
                'gender': '$user.gender',
                'godfather': '$user.godfather',
                'city': '$user.city',
                'neighborhood': '$user.neighborhood',
                'address': '$user.address',
                'observations': '$user.observations',
                'status': '$user.status',
                'updated_by': '$user.updated_by',
                'updated_at': '$user.updated_at',
            }
        }]))


def update_student(studentid, params):
    studentid = ObjectId(studentid)
    student = get_student(studentid)
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

    # Se verifica si se ha agregado algún tutor
    tutorsid = params.pop('tutorsid') if 'tutorsid' in params else []
    if len(tutorsid):
        deleted = mongo.db.user_tutors.delete_many(
            {'userid': ObjectId(studentid)})
        if not deleted:
            raise HTTPException('El estudiante no fue actualizado')
        user_tutors = [{'tutorid': ObjectId(tutorid),
                    'userid': ObjectId(studentid)} for tutorid in tutorsid]
        inserted = mongo.db.user_tutors.insert_many(user_tutors)
        if not inserted:
            raise HTTPException('El estudiante no fue actualizado')

    updated = mongo.db.users.update_one({'_id': studentid}, {'$set': params})
    if not updated:
        raise HTTPException('El estudiante no fue actualizado')
    return updated
