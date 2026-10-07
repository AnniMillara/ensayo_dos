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
    def visualizar_todos(cls):
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
            FROM tareas
            WHERE id_tarea = %(id_tarea)s;
        """
        data = {"id_tarea": id}
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
        data = {"id_tarea": id}
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
    def buscar_nombre(cls, nombre):
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
        data = {"nombre": nombre}
        resultado = connectToMySQL('esquema_tareas').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def _buscar_por_campo(cls, campo, valor):
        """Método auxiliar para búsquedas por FK."""
        query = f"""
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
            WHERE {campo} = %({campo})s;
        """
        data = {campo: valor}
        resultados = connectToMySQL('esquema_tareas').query_db(query, data)
        tareas = []
        for tarea in resultados:
            tareas.append(cls(tarea))
        return tareas

    @classmethod
    def buscar_categoria(cls, id):
        return cls._buscar_por_campo("categoria_id", id)

    @classmethod
    def buscar_estado(cls, id):
        return cls._buscar_por_campo("estado_id", id)

    @classmethod
    def buscar_prioridad(cls, id):
        return cls._buscar_por_campo("prioridad_id", id)

    @staticmethod
    def validar_tarea(datos):
        es_valido = True

        if not datos["nombre"]:
            flash("El nombre es obligatorio.", "danger")
            es_valido = False
        elif len(datos["nombre"]) < 3:
            flash("El nombre debe tener al menos 3 caracteres.", "danger")
            es_valido = False

        if not datos["descripcion"]:
            flash("La descripción es obligatoria.", "danger")
            es_valido = False

        if not datos["categoria_id"]:
            flash("Debes seleccionar una categoría.", "danger")
            es_valido = False

        if not datos["prioridad_id"]:
            flash("Debes seleccionar una prioridad.", "danger")
            es_valido = False

        if not datos["estado_id"]:
            flash("Debes seleccionar un estado.", "danger")
            es_valido = False

        return es_valido