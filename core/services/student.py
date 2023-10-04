import json
from core.app import mongo
from bson import json_util

def get_students(params: dict):
    return json.loads(json_util.dumps(mongo.db.usuario.find_one(params)))