from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from app.schemas.comment import CommentIn, CommentOut, Comments
from app.services import comment
from app.schemas.generic import Message
from app.utils import success_message

bp = APIBlueprint('comment', __name__)

@bp.post('/')
@bp.input(CommentIn, location='form_and_files')
@bp.output(Message)
@jwt_required()
def create_comment(form_and_files_data):
    '''
    Create comment
    :param data:
    '''
    try:
        form_and_files_data['userid'] = get_jwt()['_id']
        form_and_files_data['updated_by'] = get_jwt()['username']
        comment.create_comment(form_and_files_data)
        return {'message': 'Guardado exitosamente'}
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/')
@bp.output(Comments)
def get_comments():
    '''
    Get comments
    '''
    try:
        return Comments().dump({'items': comment.get_comments()})
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/<string:commentid>')
@bp.output(CommentOut)
def get_comment_detail(commentid):
    '''
    Get comment detail
    '''
    try:
        return CommentOut().dump(
            comment.get_comment_by_id(commentid))
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.patch('/<string:commentid>')
@bp.input(CommentIn)
@bp.output(Message)
def update_comment(commentid, data):
    '''
    Update comments
    :param data:
    '''
    try:
        comment.update_comment(commentid, data)
        return success_message()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.delete('/<string:commentid>')
@bp.output(Message)
def delete_comment(commentid, data):
    '''
    Delete comments
    :param data:
    '''
    try:
        comment.delete_comment(commentid, data)
        return success_message()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))
