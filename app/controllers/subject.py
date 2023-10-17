from http.client import HTTPException
from apiflask import APIBlueprint
subjects = []

bp = APIBlueprint('subject', __name__)

@bp.get('/')
def get_subjects():
    try:
        return subjects
    except Exception as e:
        raise HTTPException(500, e)

@bp.get('/subject-detail/<string:subjectid>')
def get_subject_detail(subject_id):
    try:
        return {'message': 'Subject detail'}
    except Exception as e:
        raise HTTPException(500, e)

@bp.get('/subjects-teacher/<string:teacherid>')
def get_subject_by_teacher(teacher_id):
    try:
        return {'message': 'Subjects by teacher id'}
    except Exception as e:
        raise HTTPException(500, e)

@bp.post('/')
def create_subject():
    try:
        return {'message': 'Subject creation'}
    except Exception as e:
        raise HTTPException(500, e)

@bp.patch('/')
def update_subject():
    try:
        return {'message': 'Subject update'}
    except Exception as e:
        raise HTTPException(500, e)
