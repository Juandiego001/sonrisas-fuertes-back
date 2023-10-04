from http.client import HTTPException
from app import mongo
from bson import ObjectId

def create_profile(params: dict):
    return mongo.db.perfil.insert_one(params)
                                      
def get_profiles():
    return list(mongo.db.perfil.find())

def get_profile_detail(profileid: str):
    profile = mongo.db.perfil.find_one(ObjectId(profileid))
    if not profile:
        raise HTTPException('Profile not found')
    return profile

def update_profile(profileid: str, profile: dict):
    profile = mongo.db.perfil.find_one_and_update(
        {'_id': ObjectId(profileid)},
        {'$set': profile})
    if not profile:
        raise HTTPException('Profile was not found')
    return profile