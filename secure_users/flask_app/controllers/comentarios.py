from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.usuario import Usuarios
from flask_app.models.tarea import Tareas
from flask_app.models.comentario import Comentarios


@app.route("/comentario/crear/<int:tarea_id>", methods=["POST"])
def crear_comentario(tarea_id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder comentar.", "danger")
        return redirect(url_for("inicio"))

    tarea = Tareas.buscar_id(tarea_id)
    if not tarea:
        flash("La tarea ya no existe.", "danger")
        return redirect(url_for("tareas"))

    contenido = request.form.get("contenido", "").strip()
    if not contenido:
        flash("Es necesario escribir algún mensaje antes de enviar...", "danger")
        return redirect(url_for("detalle_tarea", id=tarea_id))

    datos = {
        "contenido": contenido,
        "tarea_id": tarea_id,
        "usuario_id": session["id_usuario"]
    }

    Comentarios.guardar(datos)
    flash("Comentario enviado exitosamente.", "success")
    return redirect(url_for("detalle_tarea", id=tarea_id))


@app.route("/comentario/eliminar/<int:id>", methods=["POST"])
def eliminar_comentario(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder eliminar un comentario.", "danger")
        return redirect(url_for("inicio"))

    comentario = Comentarios.buscar_id(id)
    if not comentario:
        flash("Ups, parece que no existe ese comentario...", "danger")
        return redirect(url_for("tareas"))

    usuario = Usuarios.buscar_id(session["id_usuario"])
    if not usuario:
        session.clear()
        flash("Tu sesión no es válida. Inicia sesión de nuevo.", "danger")
        return redirect(url_for("inicio"))

    if comentario.usuario_id != usuario.id_usuario:
        flash("No tienes permiso para eliminar este comentario.", "danger")
        return redirect(url_for("detalle_tarea", id=comentario.tarea_id))

    Comentarios.eliminar(id)
    flash("Comentario eliminado exitosamente.", "success")
    return redirect(url_for("detalle_tarea", id=comentario.tarea_id))