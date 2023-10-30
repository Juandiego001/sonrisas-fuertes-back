from app import mongo


def create_user_profile(params: dict):
    return mongo.db.user_profiles.insert_one(params)
