from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.link import LinkIn, LinkOut, Links
from app.services import link
from app.schemas.generic import Message
from werkzeug.exceptions import HTTPException
from app.utils import success_message


bp = APIBlueprint('link', __name__)


@bp.post('/')
@bp.input(LinkIn)
@bp.output(Message)
@jwt_required()
def create_link(data):
    try:
        data['updated_by'] = get_jwt()['username']
        link.create_link(data)
        return success_message()
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Links)
def get_links():
    try:
        return Links().dump({'items': link.get_links()})
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:linkid>')
@bp.output(LinkOut)
def get_link_detail(linkid):
    try:
        return link.get_link_detail(linkid)
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:linkid>')
@bp.input(LinkIn)
@bp.output(Message)
@jwt_required()
def update_link(linkid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        link.update_link(linkid, data)
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))
    