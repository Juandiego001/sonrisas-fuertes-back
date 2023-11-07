from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask import jsonify, send_from_directory
from flask_jwt_extended import create_access_token, get_jwt_identity,\
    jwt_required, set_access_cookies, unset_jwt_cookies
from app.schemas.account import ChangePassword, Login, Email, Profile, Photo,\
    NewPassword
from app.services import account
from app.schemas.generic import Message
from bson.errors import InvalidId
from app.utils import success_message


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
        user = account.login(user_data)      
        data_profile = Profile().dump(user)
        access_token = create_access_token(
            identity=str(data_profile['_id']), additional_claims=data_profile)
        response = jsonify({'message': 
                            f'Bienvenido/a {user["name"]} {user["lastname"]}'})
        set_access_cookies(response, access_token)
        return response
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/logout')
def logout():
    try:
        response = jsonify({'message': 'Sesión finalizada'})
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
        account.request_reset_password(data['email'])
        return {'message':
                'Se ha enviado un correo para reestablecer la contraseña'}
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/reset-password/<string:secret>')
@bp.input(NewPassword)
def set_password(secret, data):
    '''
    Set password
    :param data:
    '''
    try:
        account.set_password(secret, data['new_password'])
        return success_message()
    except HTTPException as ex:
        abort(404, ex.description)
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
        user_detail = account.get_user_by_id(user_id).try_next()
        username = user_detail['username']

        read_permissions = account.\
            get_user_permissions(username, 'read').try_next()
        create_permissions = account.\
            get_user_permissions(username, 'create').try_next()
        update_permissions = account.\
            get_user_permissions(username, 'update').try_next()

        user_detail['abilities'] = []
        if read_permissions:
            user_detail['abilities'] += read_permissions['permissions']
        if create_permissions:
            user_detail['abilities'] += create_permissions['permissions']
        if update_permissions:
            user_detail['abilities'] += update_permissions['permissions']
            
        user_profile = Profile().dump(user_detail)
        return user_profile
    except InvalidId as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.put('/profile/photo/<string:username>')
@bp.input(Photo, location='files')
@bp.output(Message)
def upload_photo(username, files):
    try:
        account.upload_photo(username, files['photo'])
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/change-password')
@bp.input(ChangePassword)
@bp.output(Message)
@jwt_required()
def change_password(data):
    try:
        account.change_password(get_jwt_identity(), data)
        return success_message()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/photo/<string:photo_url>')
@bp.output(Photo)
def get_photo(photo_url):
    return send_from_directory('../uploads/photos/', photo_url, 
                               as_attatchment=True)