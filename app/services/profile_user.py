from app import mongo
from datetime import datetime

def create_profile_user(params: dict):
    return mongo.db.perfil_usuario.insert_one(params)
