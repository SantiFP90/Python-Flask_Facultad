from flask import (Flask, Blueprint, render_template, request, redirect, url_for, flash, jsonify)
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from utils.db import db 
from flask_marshmallow import Marshmallow
from config import DATABASE_CONNECTION_URI
from models.creaTablas import crea_tablas_DB
from strategies.estrategias import estrategias
from strategies.datoSheet import datoSheet
from strategies.Experimental.FuncionesBasicas01 import FuncionesBasicas01
from tokens.token import token
from routes.instrumentos import instrumentos
from routes.instrumentosGet import instrumentosGet
from routes.api_externa_conexion.get_login import get_login
from routes.api_externa_conexion.comprar import comprar
from routes.api_externa_conexion.operaciones import operaciones
from routes.api_externa_conexion.validaInstrumentos import validaInstrumentos
from routes.api_externa_conexion.cuenta import cuenta
from routes.api_externa_conexion.wsocket import wsocket
from routes.suscripciones import suscripciones
from cuentas.cuentaUsuarioBroker import cuentas
from fichasTokens.fichas import fichas
from usuarios.autenticacion import autenticacion
from usuarios.registrarUsuario import registrarUsuario
from usuarios.usuario import usuario
from social.imagenes.imagenesOperaciones import imagenesOperaciones
from social.media_e_mail import media_e_mail
from panelControlBroker.panelControl import panelControl
from panelControl.pcEstrategiaUs import pcEtrategiaUs
from automatizacion.programar_trigger import programar_trigger
from models.usuario import Usuario
from models.triggerEstrategia import triggerEstrategia
from models.orden import orden
from models.ficha import ficha
from models.trazaFicha import trazaFicha
from models.operacion import operacion
from models.operacionHF import operacionHF
from models.logs import logs
from models.creaTablas import creaTabla
from flask_login import LoginManager
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint, google
import schedule
import time

app = Flask(__name__, static_folder='static')
login_manager = LoginManager(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Configura el manejo de autenticación JWT
app.config['JWT_SECRET_KEY'] = '621289'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
jwt = JWTManager(app)

# Configura el blueprint de Google OAuth
blueprint = make_google_blueprint(client_id='client_id',
                                   client_secret='client_secret',
                                   scope=['profile', 'email'])
app.register_blueprint(blueprint, url_prefix='/login')

# Registrar blueprints
app.register_blueprint(logs)
app.register_blueprint(creaTabla)
app.register_blueprint(token)
app.register_blueprint(instrumentos)
app.register_blueprint(instrumentosGet)
app.register_blueprint(get_login)
app.register_blueprint(cuenta)
app.register_blueprint(cuentas)
app.register_blueprint(orden)
app.register_blueprint(comprar)
app.register_blueprint(operacion)
app.register_blueprint(operaciones)
app.register_blueprint(operacionHF)
app.register_blueprint(validaInstrumentos)
app.register_blueprint(wsocket)
app.register_blueprint(suscripciones)
app.register_blueprint(estrategias)
app.register_blueprint(datoSheet)
app.register_blueprint(autenticacion)
app.register_blueprint(registrarUsuario)
app.register_blueprint(usuario)
app.register_blueprint(imagenesOperaciones)
app.register_blueprint(media_e_mail)
app.register_blueprint(panelControl)
app.register_blueprint(pcEtrategiaUs)
app.register_blueprint(FuncionesBasicas01)
app.register_blueprint(ficha)
app.register_blueprint(trazaFicha)
app.register_blueprint(fichas)

app.secret_key = '*0984632'
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Inicializa SQLAlchemy y Marshmallow
db.init_app(app)
ma = Marshmallow(app)


##Subida al repo
MANTISBT_URL = 'http://localhost/mantisbt/api/rest/issues/'
MANTISBT_API_TOKEN = 'G2foOdwp3HxE20uoRwNWJ-S6A1TP9IP7'
MANTISBT_HEADERS = {
    'Authorization': 'Bearer ' + MANTISBT_API_TOKEN,
    'Content-Type': 'application/json'
}

@app.route('/report_issue', methods=['POST'])
def report_issue():
    print("Debajo los headers")
    print("Headers:", request.headers)
    print("JSON:", request.json)
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data received"}), 400
    issue_data = {
        "summary": data['Issue post'],
        "description": data['description'],  
        "project": {"id": data['project_id']},
        "category": data['configuracion']
    }
    response = requests.post(
        MANTISBT_URL,
        headers=MANTISBT_HEADERS,
        data=json.dumps(issue_data)
    )
    if response.status_code == 201:
        return jsonify({"message": "Issue creado exitosamente en MantisBT"}), 201
    else:
        return jsonify({"message": "Error al crear el issue", "status_code": response.status_code}), response.status_code




@app.route("/")
def entrada():  
    crea_tablas_DB()
    return redirect("index")

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    # Ciclo para ejecutar las tareas programadas
    while True:
        schedule.run_pending()
        time.sleep(1)
