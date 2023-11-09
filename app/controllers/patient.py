from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.patient import PatientIn, PatientOut, Patients
from app.services import patient
from app.schemas.generic import Message
from app.utils import success_message


bp = APIBlueprint('patient', __name__)


@bp.post('/')
@bp.input(PatientIn)
@bp.output(Message)
@jwt_required()
def create_patient(data):
    try:
        data['updated_by'] = get_jwt()['username']
        patient.create_patient(data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:patientid>')
@bp.output(PatientOut)
def get_patient_detail(patientid):
    try:
        return patient.get_patient_by_id(patientid)
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Patients)
def get_patients():
    try:
        return Patients().dump({'items': patient.get_patients()})
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:patientid>')
@bp.input(PatientIn)
@bp.output(Message)
@jwt_required()
def update_patient(patientid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        patient.update_patient(patientid, data)
        return success_message()
    except HTTPException as ex:        
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))
