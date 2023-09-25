from http.client import HTTPException
from apiflask import APIBlueprint, abort
from app.schemas.admin import AdminIn
from app import mongo

bp = APIBlueprint('admins', __name__)

# @bp.get('/')
# def get_users():
#     try:
#         users = []
#         for user in mongo.db.usuario.find({}, {'name': 1, 'lastname': 1, 'document': 1, 'username': 1, 
#                                             'password': 1, 'photo': 1 }):
#             users.append(user)
#         return {'users': users}
#     except Exception as ex:
#         abort(500, str(ex))

# @bp.post('/')
# @bp.input(UserIn)
# def create_user(user_data):
#     try:
#         users.append(user_data)
#         return {'message': 'User created successfully'}
#     except Exception as ex:
#         abort(500, str(ex))

