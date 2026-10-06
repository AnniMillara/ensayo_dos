from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL   

class Tareas:
    def __init__(self, data):
        self.id_tarea = data["id_tarea"]
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        self.categoria_id = data["categoria_id"]
        self.prioridad_id = data["prioridad_id"]
        self.estado_id = data["estado_id"]
        self.usuario_id = data["usuario_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def vizualizar_todos(cls):
        query = """
            SELECT 
                id_tarea,
                nombre,
                descripcion,
                categoria_id,
                prioridad_id,
                categoria_id,
                usuario_id,
                created_at,
                updated_at
            FROM usuarios
            ORDER BY id_tarea;
        """
        
        resultados = connectToMySQL('esquema_tareas').query_db(query)
        
        tareas = []
        for tarea in resultados:
            tareas.append(cls(tarea))
        
        return tareas

    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                id_tarea,
                nombre,
                descripcion,
                categoria_id,
                prioridad_id,
                estado_id,
                usuario_id,
                created_at,
                updated_at
            FROM usuarios
            WHERE id_tarea = %(id_tarea)s;
        """
        
        data = {
            "id_tarea" : id
        }
        resultado = connectToMySQL('esquema_tareas').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def modificar(cls, data):
        query = """
            UPDATE tareas
            SET
                nombre = %(nombre)s,
                descripcion = %(descripcion)s,
                categoria_id = %(categoria_id)s,
                prioridad_id = %(prioridad_id)s,
                estado_id = %(estado_id)s,
                usuario_id = %(usuario_id)s,
                updated_at = NOW()
            WHERE id_tarea = %(id_tarea)s;
        """
        
        return connectToMySQL('esquema_tareas').query_db(query, data)

    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM tareas
            WHERE id_tarea = %(id_tarea)s;
        """
        
        data = {
            "id_tarea": id
        }
        return connectToMySQL("esquema_tareas").query_db(query, data)

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO tareas(
                nombre,
                descripcion,
                categoria_id,
                prioridad_id,
                estado_id,
                usuario_id,
                created_at,
                updated_at
            ) VALUES (
                %(nombre)s,
                %(descripcion)s,
                %(categoria_id)s,
                %(prioridad_id)s,
                %(estado_id)s,
                %(usuario_id)s,
                NOW(),
                NOW()
            );
        """

        return connectToMySQL("esquema_tareas").query_db(query, data)

    @classmethod
    def buscar_email(cls, nombre):
        query = """
            SELECT
                id_tarea,
                nombre,
                descripcion,
                categoria_id,
                prioridad_id,
                estado_id,
                usuario_id,
                created_at,
                updated_at
            FROM tareas
            WHERE nombre = %(nombre)s;
        """
        data = {
            "nombre": nombre
        }
        resultado = connectToMySQL('esquema_tareas').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None