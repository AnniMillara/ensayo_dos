from flask_app import app
from flask_app.controllers import usuarios, tareas, estados, categorias, prioridades
if __name__ == "__main__":
    app.run(debug=True)