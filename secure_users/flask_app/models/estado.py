from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL


class Estados:
    def __init__(self, data):
        self.id_estado = data["id_estado"]
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        self.color = data["color"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def visualizar_todos(cls):
        query = """
            SELECT id_estado, nombre, descripcion, color, created_at, updated_at
            FROM estados
            ORDER BY id_estado;
        """
        resultados = connectToMySQL('esquema_tareas').query_db(query)
        estados = []
        for estado in resultados:
            estados.append(cls(estado))
        return estados

    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT id_estado, nombre, descripcion, color, created_at, updated_at
            FROM estados
            WHERE id_estado = %(id_estado)s;
        """
        data = {"id_estado": id}
        resultado = connectToMySQL('esquema_tareas').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def modificar(cls, data):
        query = """
            UPDATE estados
            SET
                nombre = %(nombre)s,
                descripcion = %(descripcion)s,
                color = %(color)s,
                updated_at = NOW()
            WHERE id_estado = %(id_estado)s;
        """
        return connectToMySQL('esquema_tareas').query_db(query, data)

    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM estados
            WHERE id_estado = %(id_estado)s;
        """
        data = {"id_estado": id}
        return connectToMySQL("esquema_tareas").query_db(query, data)

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO estados(
                nombre,
                descripcion,
                color,
                created_at,
                updated_at
            ) VALUES (
                %(nombre)s,
                %(descripcion)s,
                %(color)s,
                NOW(),
                NOW()
            );
        """
        return connectToMySQL("esquema_tareas").query_db(query, data)

    @classmethod
    def buscar_nombre(cls, nombre):
        query = """
            SELECT id_estado, nombre, descripcion, color, created_at, updated_at
            FROM estados
            WHERE nombre = %(nombre)s;
        """
        data = {"nombre": nombre}
        resultado = connectToMySQL('esquema_tareas').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @staticmethod
    def validar_estado(datos):
        es_valido = True
        if not datos["nombre"] or len(datos["nombre"]) < 3:
            flash("El nombre debe tener al menos 3 caracteres.", "danger")
            es_valido = False
        if not datos["descripcion"]:
            flash("La descripción es obligatoria.", "danger")
            es_valido = False
        if not datos.get("color"):
            flash("Debes elegir un color.", "danger")
            es_valido = False
        return es_valido