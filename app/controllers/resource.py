from http.client import HTTPException
from apiflask import APIBlueprint
from app import resources

bp = APIBlueprint('resource', __name__)

@bp.get('/')
def get_resources():
    try:
        return resources
    except Exception as e:
        raise HTTPException(500, e)

@bp.get('/resource-detail/<string:resource_id>')
def get_resource_detail(resource_id):
    try:
        return {'message': 'Resource detail'}
    except Exception as e:
        raise HTTPException(500, e)

@bp.get('/<string:subjectid>')
def get_resources_by_subject(subjectid):
    try:
        return {'message': 'Resources by subject id'}
    except Exception as e:
        raise HTTPException(500, e)

@bp.post('/')
def create_group(resource):
    try:
        return {'message': 'Resource creation'}
    except Exception as e:
        raise HTTPException(500, e)

@bp.patch('/<string:resource_id>')
def update_group(resource, resource_id):
    try:
        return {'message': 'Resource update'}
    except Exception as e:
        raise HTTPException(500, e)

