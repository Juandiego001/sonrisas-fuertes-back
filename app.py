from dotenv import load_dotenv
from flask import Flask
from firebase import firebase   
import os

load_dotenv()
app = Flask(__name__)
DATABASE_URL = os.getenv('DATABASE_URL')
firebase = firebase.FirebaseApplication(DATABASE_URL, None)

@app.route("/")
def test():
    result = firebase.get('/ingreso', None)
    return result

@app.route("/users", methods=['GET', 'POST'])
def create_user():
    result = firebase.post('/ingreso', {'usuario': 'prueba2', 'contrasena': '4231'})
    return result
