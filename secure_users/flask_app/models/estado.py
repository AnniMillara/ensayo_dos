from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL   

class Categorias:
    def __init__(self, data):
        self.id_categoria = data["id_categoria"]
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def vizualizar_todos(cls):
        query = """
            SELECT 
                id_categoria,
                nombre,
                descripcion,
                created_at,
                updated_at
            FROM categorias
            ORDER BY id_categoria;
        """
        
        resultados = connectToMySQL('esquema_tareas').query_db(query)
        
        categorias = []
        for categoria in resultados:
            categorias.append(cls(categoria))
        
        return categorias

    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                id_categoria,
                nombre,
                descripcion,
                created_at,
                updated_at
            FROM categorias
            WHERE id_categoria = %(id_categoria)s;
        """
        
        data = {
            "id_categoria" : id
        }
        resultado = connectToMySQL('esquema_tareas').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def modificar(cls, data):
        query = """
            UPDATE categorias
            SET
                nombre = %(nombre)s,
                descripcion = %(descripcion)s,
                updated_at = NOW()
            WHERE id_categoria = %(id_categoria)s;
        """
        
        return connectToMySQL('esquema_tareas').query_db(query, data)

    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM categorias
            WHERE id_categoria = %(id_prioridad)s;
        """
        
        data = {
            "id_categoria": id
        }
        return connectToMySQL("esquema_tareas").query_db(query, data)

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO categorias(
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
                id_categoria,
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