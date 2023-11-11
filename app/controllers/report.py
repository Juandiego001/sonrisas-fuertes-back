from apiflask import APIBlueprint, abort
from flask import send_file
from app.services import report


bp = APIBlueprint('report', __name__)


@bp.get('/students')
def get_students_report():
  try:
    return send_file(report.get_students_report(),
                     as_attachment=True,
                     download_name='Estudiantes - RSPD.xlsx')
  except Exception as ex:
    abort(500, str(ex))


@bp.get('/patients')
def get_patients_report():
  try:
    return send_file(report.get_patients_report(),
                     as_attachment=True,
                     download_name='Pacientes - RSPD.xlsx')
  except Exception as ex:
    abort(500, str(ex))