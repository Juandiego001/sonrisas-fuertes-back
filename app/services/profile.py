from http.client import HTTPException
from app import mongo
from bson import ObjectId


def create_profile(params: dict):
    return mongo.db.profiles.insert_one(params)


def get_profiles():
    return list(mongo.db.profiles.find())


def get_profile_detail(profileid: str):
    profile = mongo.db.profiles.find_one(ObjectId(profileid))
    if not profile:
        raise HTTPException('Perfil no encontrado')
    return profile


def update_profile(profileid: str, profile: dict):
    profile = mongo.db.profiles.find_one_and_update(
        {'_id': ObjectId(profileid)},
        {'$set': profile})
    if not profile:
        raise HTTPException('Perfil no encontrado')
    return profile