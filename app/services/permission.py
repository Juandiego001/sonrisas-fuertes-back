from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId

def update_permission(permissionid: str, params: dict):
    params['updated_at'] = datetime.now()
    permission = mongo.db.permiso.find_one_and_update(permissionid, params)
    if not permission:
        raise HTTPException('Permission not found')
    return permission

def get_permissions_by_profile(profileid):
    return mongo.db.permiso.find({'profileid': ObjectId(profileid)})
