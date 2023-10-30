import json
from werkzeug.exceptions import HTTPException
from threading import Timer
from flask import render_template
from app import app, smtp_config, mongo
from app.utils import send_mail
from bson import json_util, ObjectId


def login(user_data: dict):
    user = mongo.db.users.find_one(
        {'username': user_data['username'], 
         'password': user_data['password']})
    if not user:
        raise HTTPException('Usuario o contraseña incorrectos')
    else:
        return user


def get_user_by_id(userid: str):
    user = mongo.db.users.aggregate([{
            '$lookup': {
                'from': 'user_profiles', 
                'localField': '_id', 
                'foreignField': 'userid', 
                'pipeline': [
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
                    }
                ], 
                'as': 'user_profile'
            }
        }, {
            '$match': {
                '$expr': {
                    '$eq': [
                        '$_id', ObjectId(userid)
                    ]
                }
            }
        }, {
            '$project': {
                'username': 1, 
                'name': 1, 
                'lastname': 1, 
                'document': 1, 
                'email': 1, 
                'profiles': '$user_profile.profile.name'
            }
        }
    ])

    if not user:
        raise HTTPException('Usuario no encontrado')
    return user


def get_user_by_email(email: str):
    return mongo.db.users.find_one({'email': email})


def get_user_permissions(username: str, permission: str):
    return mongo.db.user_profiles.aggregate(
        [{
            '$lookup': {
                'from': 'permissions', 
                'localField': 'profileid', 
                'foreignField': 'profileid', 
                'let': {
                    f'{permission}': f'${permission}'
                },
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'modules', 
                            'localField': 'moduleid', 
                            'foreignField': '_id', 
                            'as': 'modules'
                        }
                    }, {
                        '$unwind': {
                            'path': '$modules'
                        }
                    }, {
                        '$match': {
                            '$expr': {
                                '$eq': [
                                    f'${permission}', True
                                ]
                            }
                        }
                    }, {
                        '$addFields': {
                            'subject': '$modules.name',
                            'action': f'{permission}',
                        }
                    }
                ], 
                'as': 'permissions'
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
                '$expr': {
                    '$eq': [
                        '$user.username', username
                    ]
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'permissions.action': 1,
                'permissions.subject': 1
            }
        }
    ])


def request_reset_password(email: str):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException('Usuario no encontrado')
    userid = json.loads(json_util.dumps(user))
    link = f'{app.config["URL_PASSWORD_RESET"]}/{userid["_id"]["$oid"]}'
    message = render_template(
        'mail/reset-password.html',
        link=link)
    with app.app_context():
        t = Timer(0, send_mail, args=(smtp_config,
                                      'Reestablece tu contraseña',
                                      email, message,))
        t.start()


def set_password(userid: str, new_password: str):
    updated = mongo.db.users.find_one_and_update(
        {'_id': ObjectId(userid)},
        {'$set': {'password': new_password}})
    if not updated:
        raise HTTPException('Usuario no encontrado')


def change_password(userid: str, data: dict):
    updated = mongo.db.users.find_one_and_update(
        {'_id': ObjectId(userid), 'password': data['current_password']},
        {'$set': {'password': data['new_password']}})
    if not updated:
        raise HTTPException('No hay coincidencia con la contraseña actual')
