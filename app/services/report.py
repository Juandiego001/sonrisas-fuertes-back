import pandas as pd
import io
from app.services import student

def get_students_report():
  buffer = io.BytesIO()
  students = student.get_students()
  students_df = pd.DataFrame(students)
  writer = pd.ExcelWriter(buffer)
  students_df.to_excel(writer, sheet_name='Estudiantes')
  writer.save()
  buffer.seek(0)
  return buffer

def get_patients_report():
  buffer = io.BytesIO()
  students = student.get_students({'user.username': None})
  students_df = pd.DataFrame(students)
  writer = pd.ExcelWriter(buffer)
  students_df.to_excel(writer, sheet_name='Pacientes')
  writer.save()
  buffer.seek(0)
  return buffer