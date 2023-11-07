import json
from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from app.schemas.delivery import DeliveryIn, DeliveryOut, Deliveries
from app.services import delivery
from app.schemas.generic import Message
from app.utils import success_message


bp = APIBlueprint('delivery', __name__)


@bp.post('/')
@bp.input(DeliveryIn, location='files')
@bp.output(Message)
@jwt_required()
def create_delivery(files_data):
    '''
    Create delivery for activities
    :param data:
    '''
    try:
        files_data['userid'] = get_jwt()['_id']
        if 'links' in files_data:
            files_data['links'] = \
                [json.loads(link) for link in files_data['links']]
        files_data['updated_by'] = get_jwt()['username']
        delivery.create_delivery(files_data)
        return success_message()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Deliveries)
def get_deliveries():
    '''
    Get deliveries
    '''
    try:
        return Deliveries().dump({'items': delivery.get_deliveries()})
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:deliveryid>')
@bp.output(DeliveryOut)
def get_delivery_detail(deliveryid):
    '''
    Get delivery detail
    '''
    try:
        return delivery.get_delivery_by_id(deliveryid)
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:deliveryid>')
@bp.input(DeliveryIn, location='files')
@bp.output(Message)
def update_delivery(deliveryid, files_data):
    '''
    Update delivery
    :param data:
    '''
    try:
        # Se implementó este código por la imposibilidad de enviar
        # un arreglo de strings a través del esquema de entrada
        if 'links' in files_data:
            files_data['links'] = \
                [json.loads(link) for link in files_data['links']]
        delivery.update_delivery(deliveryid, files_data)
        return success_message()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.delete('/<string:deliveryid>')
@bp.output(Message)
@jwt_required()
def delete_delivery(deliveryid):
    '''
    Delete delivery
    '''
    try:
        delivery.delete_delivery(deliveryid)
        return success_message()
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))
