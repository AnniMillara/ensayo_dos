from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL


class Comentarios:
    def __init__(self, data):
        self.id_comentario = data["id_comentario"]
        self.contenido = data["contenido"]
        self.usuario_id = data["usuario_id"]
        self.tarea_id = data["tarea_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def visualizar_todos(cls):
        query = """
            SELECT 
                id_comentario,
                contenido,
                usuario_id,
                tarea_id,
                created_at,
                updated_at
            FROM comentarios
            ORDER BY id_comentario;
        """
        resultados = connectToMySQL('esquema_tareas').query_db(query)
        comentarios = []
        for comentario in resultados:
            comentarios.append(cls(comentario))
        return comentarios

    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                id_comentario,
                contenido,
                usuario_id,
                tarea_id,
                created_at,
                updated_at
            FROM comentarios
            WHERE id_comentario = %(id_comentario)s;
        """
        data = {"id_comentario": id}
        resultado = connectToMySQL('esquema_tareas').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def modificar(cls, data):
        query = """
            UPDATE comentarios
            SET
                contenido = %(contenido)s,
                updated_at = NOW()
            WHERE id_comentario = %(id_comentario)s;
        """
        return connectToMySQL('esquema_tareas').query_db(query, data)

    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM comentarios
            WHERE id_comentario = %(id_comentario)s;
        """
        data = {"id_comentario": id}
        return connectToMySQL("esquema_tareas").query_db(query, data)

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO comentarios(
                contenido,
                usuario_id,
                tarea_id,
                created_at,
                updated_at
            ) VALUES (
                %(contenido)s,
                %(usuario_id)s,
                %(tarea_id)s,
                NOW(),
                NOW()
            );
        """
        return connectToMySQL("esquema_tareas").query_db(query, data)

    @classmethod
    def buscar_por_tarea(cls, tarea_id):
        query = """
            SELECT
                id_comentario,
                contenido,
                usuario_id,
                tarea_id,
                created_at,
                updated_at
            FROM comentarios
            WHERE tarea_id = %(tarea_id)s
            ORDER BY created_at DESC;
        """
        data = {"tarea_id": tarea_id}
        resultados = connectToMySQL('esquema_tareas').query_db(query, data)
        comentarios = []
        for comentario in resultados:
            comentarios.append(cls(comentario))
        return comentarios