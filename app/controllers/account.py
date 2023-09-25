from http.client import HTTPException
from apiflask import APIBlueprint, abort
from flask import jsonify, request, send_from_directory
from flask_jwt_extended import create_access_token, get_jwt_identity,\
    jwt_required, set_access_cookies, unset_jwt_cookies
from app.schemas.account import Login, Email, Profile, Photo
from app import users
from app.services.account import request_reset_password, get_user_by_id,\
    account_login
from app.schemas.generic import Message
from bson.errors import InvalidId

bp = APIBlueprint('account', __name__)

@bp.post('/login')
@bp.input(Login)
@bp.output(Message)
def login(user_data):
    '''
    Login
    :param data:
    '''
    try:
        user = account_login(user_data)      
        data_profile = Profile().dump(user)
        access_token = create_access_token(
            identity=str(user['_id']['$oid']), additional_claims=data_profile)
        response = jsonify({'message': 
                            f'Bienvenido/a {user["name"]} {user["lastname"]}'})
        set_access_cookies(response, access_token)
        return response
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/logout')
def logout():
    try:
        response = jsonify({'message': 'Session ended'})
        unset_jwt_cookies(response)
        return response
    except Exception as ex:
        abort(500, str(ex))

@bp.post('/reset-password')
@bp.input(Email)
def reset_password(data):
    '''
    Reset password
    :param data:
    '''
    try:
        request_reset_password(data['email'])
        return {'message': 'Sent email successfully'}
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/profile')
@bp.output(Profile)
@jwt_required(optional=True)
def get_profile():
    '''
    Get the current session
    '''
    try:
        if not get_jwt_identity():
            return {}
        user_id = get_jwt_identity()
        user_detail = get_user_by_id(user_id)
        user_profile = Profile().dump(user_detail)
        return user_profile
    except InvalidId as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/photo/<string:photo_url>')
@bp.output(Photo)
def get_photo(photo_url):
    return send_from_directory('../uploads/photos/', photo_url, as_attatchment=True)