from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Clave secreta para las sesiones (cámbiala por algo más seguro en producción)
app.secret_key = "tasktrack_clave_secreta_2026"

# Bcrypt para hashear contraseñas
bcrypt = Bcrypt(app)

# Importar los controladores DESPUÉS de crear app y bcrypt
from flask_app.controllers import usuarios
from flask_app.controllers import tareas
from flask_app.controllers import categorias
from flask_app.controllers import prioridades
from flask_app.controllers import estados
from flask_app.controllers import comentarios