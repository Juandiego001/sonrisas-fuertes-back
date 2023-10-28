from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from app.schemas.publication import PublicationIn, PublicationOut, Publications
from app.schemas.comment import Comments
from app.services import publication
from app.schemas.generic import Message
from app.utils import success_message

bp = APIBlueprint('publication', __name__)

@bp.post('/')
@bp.input(PublicationIn)
@bp.output(Message)
@jwt_required()
def create_publication(data):
    '''
    Create publication that could be an activiy
    :param data:
    '''
    try:
        data['userid'] = get_jwt()['_id']
        data['updated_by'] = get_jwt()['username']
        publication.create_publication(data)
        return {'message': 'Guardado exitosamente'}
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/')
@bp.output(Publications)
def get_publications():
    '''
    Get publications
    '''
    try:
        return Publications().dump({'items': publication.get_publications()})
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:publicationid>')
@bp.output(PublicationOut)
def get_publication_detail(publicationid):
    '''
    Get publication detail
    '''
    try:
        publications =  publication.get_publication_by_id(publicationid).next()
        comments = publications.pop('comments')
        publications = PublicationOut().dump(publications)
        comments = Comments().dump({'items': comments})
        publications['comments'] = comments['items']
        return publications
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:publicationid>')
@bp.input(PublicationIn)
@bp.output(Message)
def update_publication(publicationid, data):
    '''
    Update publications
    :param data:
    '''
    try:
        publication.update_publication(publicationid, data)
        return success_message()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/activities')
@bp.output(Publications)
def get_activites():
    '''
    Get activities
    '''
    try:
        return Publications().dump(
            {'items': publication.get_publications(isActivity=True)})
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/activities/<string:activityid>')
@bp.output(PublicationOut)
@jwt_required()
def get_activity_detail(activityid):
    '''
    Get activity detail
    '''
    try:
        publications =  publication.get_activity_by_id(
            activityid, get_jwt()['username']).next()
        publications = PublicationOut().dump(publications)
        return publications
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))