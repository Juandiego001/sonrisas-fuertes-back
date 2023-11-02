import json
from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from app.schemas.publication import PublicationIn, PublicationOut, Publications
from app.services import publication
from app.schemas.generic import Message
from app.utils import success_message


bp = APIBlueprint('publication', __name__)


@bp.post('/')
@bp.input(PublicationIn, location='files')
@bp.output(Message)
@jwt_required()
def create_publication(files_data):
    '''
    Create publication
    :param data:
    '''
    try:
        files_data['userid'] = get_jwt()['_id']
        if 'links' in files_data:
            files_data['links'] = \
                [json.loads(link) for link in files_data['links']]
        files_data['userid'] = get_jwt()['_id']
        files_data['updated_by'] = get_jwt()['username']
        publication.create_publication(files_data)
        return success_message()
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
        return publication.get_publication_by_id(publicationid).next()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:publicationid>')
@bp.input(PublicationIn, location='files')
@bp.output(Message)
def update_publication(publicationid, files_data):
    '''
    Update publications
    :param data:
    '''
    try:
        # Se implementó este código por la imposibilidad de enviar
        # un arreglo de strings a través del esquema de entrada
        if 'links' in files_data:
            files_data['links'] = \
                [json.loads(link) for link in files_data['links']]
            files_data['updated_by'] = get_jwt()['username']
        publication.update_publication(publicationid, files_data)
        return success_message()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))