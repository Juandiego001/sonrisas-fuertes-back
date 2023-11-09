from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId
from app.services.profile_user import create_user_profile


def verify_if_patient_exists(params: dict):
    return mongo.db.users.find_one(params)


def create_patient(params: dict):
    patient = verify_if_patient_exists({'document': params['document']})
    if patient:
        raise HTTPException('El usuario ya existe')
    params['status'] = 'PENDING'
    params['updated_at'] = datetime.now()
    profileid = mongo.db.profiles.find_one({'name': 'Estudiante'})['_id']

    tutorsid = params.pop('tutorsid') if 'tutorsid' in params else []
    patientid = mongo.db.users.insert_one(params).inserted_id

    if len(tutorsid):
        user_tutors = [{'tutorid': ObjectId(tutorid),
                        'userid': ObjectId(patientid)} for tutorid in tutorsid]
        mongo.db.user_tutors.insert_many(user_tutors)

    return create_user_profile({
        'userid': patientid,
        'profileid': profileid
    })
        

def get_patient(patientid: str):
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
                    {'user._id': ObjectId(patientid)}
                ]
            },
        }, {
            '$project': {
                '_id': '$user._id',
                'name': '$user.name',
                'lastname': '$user.lastname',
                'document': '$user.document',
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


def get_patient_by_id(patientid: str):
    patient = verify_if_patient_exists({'_id': ObjectId(patientid)})
    if not patient:
        raise HTTPException('Paciente no encontrado')
    return get_patient(patientid)


def get_patients(query: dict = {}):
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


def update_patient(patientid, params):
    patientid = ObjectId(patientid)
    patient = get_patient(patientid)
    if not patient:
        raise HTTPException('Estudiante no encontrado')

    if 'document' in params and patient['document'] != params['document'] and\
    verify_if_patient_exists({'document': params['document']}):
        raise HTTPException('El usuario ya existe')
    
    params['updated_at'] = datetime.now()

    # Se verifica si se ha agregado algún tutor
    tutorsid = params.pop('tutorsid') if 'tutorsid' in params else []
    if len(tutorsid):
        deleted = mongo.db.user_tutors.delete_many(
            {'userid': ObjectId(patientid)})
        if not deleted:
            raise HTTPException('El paciente no fue actualizado')
        user_tutors = [{'tutorid': ObjectId(tutorid),
                    'userid': ObjectId(patientid)} for tutorid in tutorsid]
        inserted = mongo.db.user_tutors.insert_many(user_tutors)
        if not inserted:
            raise HTTPException('El paciente no fue actualizado')

    updated = mongo.db.users.update_one({'_id': patientid}, {'$set': params})
    if not updated:
        raise HTTPException('El paciente no fue actualizado')
    return updated
