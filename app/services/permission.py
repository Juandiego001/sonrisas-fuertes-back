from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId

def update_permission(permissionid: str, params: dict):
    params['updated_at'] = datetime.now()
    permission = mongo.db.permissions.find_one_and_update(permissionid, params)
    if not permission:
        raise HTTPException('Permiso no encontrado')
    return permission

def get_permissions_by_profile(profileid):
    return mongo.db.permissions.find({'profileid': ObjectId(profileid)})
