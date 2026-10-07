from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "tasktrack_clave_secreta_2026"
bcrypt = Bcrypt(app)

from flask_app.controllers import usuarios
from flask_app.controllers import tareas
from flask_app.controllers import categorias
from flask_app.controllers import prioridades
from flask_app.controllers import estados
from flask_app.controllers import comentarios