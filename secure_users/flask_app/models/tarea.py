from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL


class Tareas:
    def __init__(self, data):
        self.id_tarea = data["id_tarea"]
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        self.fecha_limite = data["fecha_limite"]
        self.categoria_id = data["categoria_id"]
        self.prioridad_id = data["prioridad_id"]
        self.estado_id = data["estado_id"]
        self.usuario_id = data["usuario_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # Campos extra de los JOINs
        self.categoria_nombre = data.get("categoria_nombre")
        self.prioridad_nombre = data.get("prioridad_nombre")
        self.estado_nombre = data.get("estado_nombre")
        self.estado_color = data.get("estado_color")
        self.creador_nombre = data.get("creador_nombre")

    @classmethod
    def visualizar_todos(cls):
        query = """
            SELECT
                t.id_tarea, t.nombre, t.descripcion, t.fecha_limite,
                t.categoria_id, c.nombre AS categoria_nombre,
                t.prioridad_id, p.nombre AS prioridad_nombre,
                t.estado_id, e.nombre AS estado_nombre, e.color AS estado_color,
                t.usuario_id, u.nombre AS creador_nombre,
                t.created_at, t.updated_at
            FROM tareas t
            JOIN categorias c ON t.categoria_id = c.id_categoria
            JOIN prioridades p ON t.prioridad_id = p.id_prioridad
            JOIN estados e ON t.estado_id = e.id_estado
            JOIN usuarios u ON t.usuario_id = u.id_usuario
            ORDER BY t.fecha_limite ASC;
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
                t.id_tarea, t.nombre, t.descripcion, t.fecha_limite,
                t.categoria_id, c.nombre AS categoria_nombre,
                t.prioridad_id, p.nombre AS prioridad_nombre,
                t.estado_id, e.nombre AS estado_nombre, e.color AS estado_color,
                t.usuario_id, u.nombre AS creador_nombre,
                t.created_at, t.updated_at
            FROM tareas t
            JOIN categorias c ON t.categoria_id = c.id_categoria
            JOIN prioridades p ON t.prioridad_id = p.id_prioridad
            JOIN estados e ON t.estado_id = e.id_estado
            JOIN usuarios u ON t.usuario_id = u.id_usuario
            WHERE t.id_tarea = %(id_tarea)s;
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
                fecha_limite = %(fecha_limite)s,
                categoria_id = %(categoria_id)s,
                prioridad_id = %(prioridad_id)s,
                estado_id = %(estado_id)s,
                updated_at = NOW()
            WHERE id_tarea = %(id_tarea)s;
        """
        return connectToMySQL('esquema_tareas').query_db(query, data)

    @classmethod
    def eliminar(cls, id):
        query = "DELETE FROM tareas WHERE id_tarea = %(id_tarea)s;"
        data = {"id_tarea": id}
        return connectToMySQL("esquema_tareas").query_db(query, data)

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO tareas(
                nombre, descripcion, fecha_limite,
                categoria_id, prioridad_id, estado_id, usuario_id,
                created_at, updated_at
            ) VALUES (
                %(nombre)s, %(descripcion)s, %(fecha_limite)s,
                %(categoria_id)s, %(prioridad_id)s, %(estado_id)s, %(usuario_id)s,
                NOW(), NOW()
            );
        """
        return connectToMySQL("esquema_tareas").query_db(query, data)

    @classmethod
    def _buscar_por_campo(cls, campo, valor):
        query = f"""
            SELECT
                t.id_tarea, t.nombre, t.descripcion, t.fecha_limite,
                t.categoria_id, c.nombre AS categoria_nombre,
                t.prioridad_id, p.nombre AS prioridad_nombre,
                t.estado_id, e.nombre AS estado_nombre, e.color AS estado_color,
                t.usuario_id, t.created_at, t.updated_at
            FROM tareas t
            JOIN categorias c ON t.categoria_id = c.id_categoria
            JOIN prioridades p ON t.prioridad_id = p.id_prioridad
            JOIN estados e ON t.estado_id = e.id_estado
            WHERE t.{campo} = %({campo})s;
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

    @classmethod
    def contar_por_estado(cls, usuario_id):
        """Devuelve totales para el resumen: total, pendientes, en progreso, completadas."""
        query = """
            SELECT e.nombre AS estado, COUNT(*) AS total
            FROM tareas t
            JOIN estados e ON t.estado_id = e.id_estado
            WHERE t.usuario_id = %(usuario_id)s
            GROUP BY e.nombre;
        """
        data = {"usuario_id": usuario_id}
        return connectToMySQL('esquema_tareas').query_db(query, data)

    @classmethod
    def proximas(cls, usuario_id, limite=5):
        """Tareas próximas a vencer (más cercanas en fecha)."""
        query = """
            SELECT
                t.id_tarea, t.nombre, t.fecha_limite,
                DATEDIFF(t.fecha_limite, CURDATE()) AS dias_restantes
            FROM tareas t
            WHERE t.usuario_id = %(usuario_id)s
              AND t.fecha_limite >= CURDATE()
            ORDER BY t.fecha_limite ASC
            LIMIT %(limite)s;
        """
        data = {"usuario_id": usuario_id, "limite": limite}
        return connectToMySQL('esquema_tareas').query_db(query, data)

    @staticmethod
    def validar_tarea(datos):
        es_valido = True

        if not datos["nombre"]:
            flash("El título es obligatorio.", "danger")
            es_valido = False
        elif len(datos["nombre"]) < 3:
            flash("El título debe tener al menos 3 caracteres.", "danger")
            es_valido = False

        if not datos["descripcion"]:
            flash("La descripción es obligatoria.", "danger")
            es_valido = False

        if not datos["fecha_limite"]:
            flash("La fecha límite es obligatoria.", "danger")
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