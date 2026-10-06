import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOMBRE_REGEX = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$')          
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d).{8,}$')     

class Usuarios:
    def __init__(self, data):
        self.id_usuario = data["id_usuario"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.contrasena = data["contrasena"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def vizualizar_todos(cls):
        query = """
            SELECT 
                id_usuario,
                nombre,
                apellido,
                email,
                contrasena,
                created_at,
                updated_at
            FROM usuarios
            ORDER BY id_usuario;
        """
        
        resultados = connectToMySQL('esquema_tareas').query_db(query)
        
        usuarios = []
        for usuario in resultados:
            usuarios.append(cls(usuario))
        
        return usuarios
    
    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                id_usuario,
                nombre,
                apellido,
                email,
                contrasena,
                created_at,
                updated_at
            FROM usuarios
            WHERE id_usuario = %(id_usuario)s;
        """
        
        data = {
            "id_usuario" : id
        }
        resultado = connectToMySQL('esquema_tareas').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None
    
    @classmethod
    def modificar(cls, data):
        query = """
            UPDATE usuarios
            SET
                nombre = %(nombre)s,
                apellido = %(apellido)s,
                email = %(email)s,
                contrasena = %(contrasena)s,
                updated_at = NOW()
            WHERE id_usuario = %(id_usuario)s;
        """
        
        return connectToMySQL('esquema_tareas').query_db(query, data)
    
    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM usuarios
            WHERE id_usuario = %(id_usuario)s;
        """
    
        data = {
            "id_usuario": id
        }
        return connectToMySQL("esquema_tareas").query_db(query, data)
    
    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO usuarios(
                nombre,
                apellido,
                email,
                contrasena,
                created_at,
                updated_at
            ) VALUES (
                %(nombre)s,
                %(apellido)s,
                %(email)s,
                %(contrasena)s,
                NOW(),
                NOW()
            );
        """
        
        return connectToMySQL("esquema_tareas").query_db(query, data)
    
    @classmethod
    def buscar_email(cls, email):
        query = """
            SELECT
                id_usuario,
                nombre,
                apellido,
                email,
                contrasena,
                created_at,
                updated_at
            FROM usuarios
            WHERE email = %(email)s;
        """
        data = {
            "email": email
        }
        resultado = connectToMySQL('esquema_tareas').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None
    
    @staticmethod
    def validar_usuario(datos, id_usuario=None):
        es_valido = True

        if not datos["nombre"].strip():
            flash("El nombre es obligatorio.", "danger")
            es_valido = False
        elif not NOMBRE_REGEX.match(datos["nombre"].strip()):
            flash("El nombre solo debe contener letras.", "danger")
            es_valido = False
        elif len(datos["nombre"].strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "danger")
            es_valido = False

        if not datos["apellido"].strip():
            flash("El apellido es obligatorio.", "danger")
            es_valido = False
        elif not NOMBRE_REGEX.match(datos["apellido"].strip()):
            flash("El apellido solo debe contener letras.", "danger")
            es_valido = False
        elif len(datos["apellido"].strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "danger")
            es_valido = False

        if not datos["email"].strip():
            flash("El email es obligatorio.", "danger")
            es_valido = False
        elif not EMAIL_REGEX.match(datos["email"].strip()):
            flash("El email no tiene un formato válido.", "danger")
            es_valido = False
        else:
            existente = Usuarios.buscar_email(datos["email"].strip())
            if existente and existente.id_usuario != id_usuario:
                flash("El email ya está registrado.", "danger")
                es_valido = False

        if not datos["contrasena"]:
            flash("La contraseña es obligatoria.", "danger")
            es_valido = False
        elif not PASSWORD_REGEX.match(datos["contrasena"]):
            flash("La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.", "danger")
            es_valido = False

        if datos.get("confirmar_contrasena") is not None:
            if datos["contrasena"] != datos["confirmar_contrasena"]:
                flash("Las contraseñas no coinciden.", "danger")
                es_valido = False

        return es_valido