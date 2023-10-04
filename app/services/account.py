import json
from werkzeug.exceptions import HTTPException
from secrets import token_urlsafe
from threading import Timer
from flask import render_template
from app import app, smtp_config, mongo
from app.utils import send_mail
from bson import json_util, ObjectId

def account_login(user_data: dict):
    user = mongo.db.usuario.find_one(
        {'username': user_data['username'], 
         'password': user_data['password']})
    if not user:
        raise HTTPException('Usuario o contraseña incorrectos')
    else:
        return user

def get_user_detail(email: str):
    return mongo.db.usuario.find_one({'email': email})

def get_user_by_id(userid: str):
    return mongo.db.usuario.find_one(ObjectId(userid))

def get_user_permissions(userid: str):
    mongo.db.permisos.aggregate([{
        '$lookup': {
            'from': 'perfil', 
            'localField': 'profileid', 
            'foreignField': '_id', 
            'let': {
                'profileid': '$_id'
            }, 
            'pipeline': [
                {
                    '$lookup': {
                        'from': 'perfil_usuario', 
                        'let': {
                            'profile_pid': '$profileid', 
                            'profile_uid': '$userid'
                        }, 
                        'pipeline': [
                            {
                                '$lookup': {
                                    'from': 'usuario', 
                                    'localField': 'userid', 
                                    'foreignField': '_id', 
                                    'as': 'user'
                                }
                            }
                        ], 
                        'as': 'profile_user'
                    }
                }
            ], 
            'as': 'profile'
        }
    }, {
        '$unwind': {
            'path': '$profile'
        }
    }, {
        '$match': {
            'profile.profile_user.user.username': 'juan_diego'
        }
    }])

    mongo.db.permisos


    return ''

def request_reset_password(email: str):
    user = get_user_detail(email)
    if not user:
        raise HTTPException('User not found')
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

def set_account_password(userid: str, new_password: str):
    return mongo.db.usuario.find_one_and_update(
        {'_id': ObjectId(userid)},
        {'$set': {'password': new_password}})

