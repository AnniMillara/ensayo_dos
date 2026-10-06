from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("ClaveMuySegura", "clave_por_defecto_larga_y_unica_1234567890")

bcrypt = Bcrypt(app)