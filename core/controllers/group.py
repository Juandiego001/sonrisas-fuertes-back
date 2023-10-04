from http.client import HTTPException
from apiflask import APIBlueprint
from core.app import groups
from core.schemas.group import GroupIn

bp = APIBlueprint('group', __name__)

@bp.get('/')
def get_groups():
    try:
        return groups
    except Exception as e:
        raise HTTPException(500, e)

@bp.get('/<string:teacherid>')
def get_groups_by_teacher(teacherid):
    try:
        return {'message': 'Groups by teacher id'}
    except Exception as e:
        raise HTTPException(500, e)

@bp.post('/')
@bp.input(GroupIn)
def create_group(group):
    try:
        print('group', group)
        groups.append(group)
        return {'message': 'Group creation'}
    except Exception as e:
        raise HTTPException(e)

@bp.patch('/<string:groupid>')
def update_group(group, groupid):
    try:
        return {'message': 'Group update'}
    except Exception as e:
        raise HTTPException(500, e)

