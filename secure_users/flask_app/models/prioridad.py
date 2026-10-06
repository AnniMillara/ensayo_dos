from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL   

class Prioridades:
    def __init__(self, data):
        self.id_prioridad = data["id_tarea"]
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def vizualizar_todos(cls):
        query = """
            SELECT 
                id_prioridad,
                nombre,
                descripcion,
                created_at,
                updated_at
            FROM prioridades
            ORDER BY id_prioridad;
        """
        
        resultados = connectToMySQL('esquema_tareas').query_db(query)
        
        prioridades = []
        for prioridad in resultados:
            prioridades.append(cls(prioridad))
        
        return prioridades

    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                id_prioridad,
                nombre,
                descripcion,
                created_at,
                updated_at
            FROM prioridades
            WHERE id_prioridad = %(id_prioridad)s;
        """
        
        data = {
            "id_prioridad" : id
        }
        resultado = connectToMySQL('esquema_tareas').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def modificar(cls, data):
        query = """
            UPDATE prioridades
            SET
                nombre = %(nombre)s,
                descripcion = %(descripcion)s,
                updated_at = NOW()
            WHERE id_prioridad = %(id_prioridad)s;
        """
        
        return connectToMySQL('esquema_tareas').query_db(query, data)

    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM prioridades
            WHERE id_prioridad = %(id_prioridad)s;
        """
        
        data = {
            "id_prioridad": id
        }
        return connectToMySQL("esquema_tareas").query_db(query, data)

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO prioridades(
                nombre,
                descripcion,
                created_at,
                updated_at
            ) VALUES (
                %(nombre)s,
                %(descripcion)s,
                NOW(),
                NOW()
            );
        """

        return connectToMySQL("esquema_tareas").query_db(query, data)

    @classmethod
    def buscar_nombre(cls, nombre):
        query = """
            SELECT
                id_prioridad,
                nombre,
                descripcion,
                created_at,
                updated_at
            FROM prioridades
            WHERE nombre = %(nombre)s;
        """
        data = {
            "nombre": nombre
        }
        resultado = connectToMySQL('esquema_tareas').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None