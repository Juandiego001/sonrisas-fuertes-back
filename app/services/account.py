from http.client import HTTPException
from secrets import token_urlsafe
from threading import Timer
from flask import render_template
from app import app, smtp_config, mongo
from app.utils import send_mail
import json
from bson import json_util, objectid

def account_login(user_data: dict):
    return json.loads(json_util.dumps(mongo.db.usuario.find_one(
        {'username': user_data['username'], 
         'password': user_data['password']})))

def request_reset_password(email: str):
    secret = token_urlsafe(16)
    link = f'{app.config["URL_PASSWORD_RESET"]}/{secret}'
    message = render_template(
        'mail/reset-password.html',
        link=link)
    with app.app_context():
        t = Timer(0, send_mail, args=(smtp_config,
                                      'Reestablece tu contraseña',
                                      email, message,))
        t.start()

def get_user_detail(params: str):
    return ''

def get_user_by_id(user_id: str):
    the_id = objectid.ObjectId(user_id)
    return json.loads(json_util.dumps(mongo.db.usuario.find_one(
        {'_id': the_id})))
