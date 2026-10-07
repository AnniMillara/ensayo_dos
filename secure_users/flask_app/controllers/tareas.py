from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.tarea import Tareas
from flask_app.models.usuario import Usuarios
from flask_app.models.categoria import Categorias
from flask_app.models.comentario import Comentarios
from flask_app.models.prioridad import Prioridades
from flask_app.models.estado import Estados


@app.route("/tareas")
def tareas():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    tareas = Tareas.visualizar_todos()
    return render_template("tareas.html", tareas=tareas)


@app.route("/tareas/detalle/<int:id>")
def detalle_tarea(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    tarea = Tareas.buscar_id(id)
    if not tarea:
        flash("Ups, parece que esa tarea no existe.", "danger")
        return redirect(url_for("tareas"))

    comentarios = Comentarios.buscar_por_tarea(id)

    return render_template(
        "tarea_detalle.html",
        tarea=tarea,
        comentarios=comentarios
    )


@app.route("/tareas/nueva")
def nueva_tarea():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    return render_template(
        "nueva_tarea.html",
        categorias=Categorias.visualizar_todos(),
        prioridades=Prioridades.visualizar_todos(),
        estados=Estados.visualizar_todos()
    )


@app.route("/tareas/crear", methods=["POST"])
def crear_tarea():
    if "id_usuario" not in session:
        flash("Inicia sesión para poder ingresar una tarea.", "danger")
        return redirect(url_for("tareas"))

    usuario = Usuarios.buscar_id(session["id_usuario"])
    if not usuario:
        session.clear()
        flash("Tu sesión ya no es válida. Inicia sesión de nuevo.", "danger")
        return redirect(url_for("inicio"))

    datos = {
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "categoria_id": request.form.get("categoria_id", "").strip(),
        "prioridad_id": request.form.get("prioridad_id", "").strip(),
        "estado_id": request.form.get("estado_id", "").strip(),
        "usuario_id": session["id_usuario"]
    }

    if not Tareas.validar_tarea(datos):
        return render_template(
            "nueva_tarea.html",
            datos=datos,
            categorias=Categorias.visualizar_todos(),
            prioridades=Prioridades.visualizar_todos(),
            estados=Estados.visualizar_todos()
        )

    Tareas.guardar(datos)
    flash("Tarea guardada correctamente.", "success")
    return redirect(url_for('tareas'))


@app.route("/tareas/editar/<int:id>")
def editar_tarea(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    tarea = Tareas.buscar_id(id)
    if not tarea:
        flash("La tarea no existe.", "danger")
        return redirect(url_for("tareas"))

    if tarea.usuario_id != session["id_usuario"]:
        flash("No tienes permiso para editar esta tarea.", "danger")
        return redirect(url_for("tareas"))

    return render_template(
        "editar_tarea.html",
        tarea=tarea,
        categorias=Categorias.visualizar_todos(),
        prioridades=Prioridades.visualizar_todos(),
        estados=Estados.visualizar_todos()
    )


@app.route("/tareas/modificar/<int:id>", methods=["POST"])
def modificar_tarea(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder modificar una tarea.", "danger")
        return redirect(url_for("tareas"))

    tarea = Tareas.buscar_id(id)
    if not tarea:
        flash("Ups, parece que la tarea ya no existe...", "danger")
        return redirect(url_for("tareas"))

    usuario = Usuarios.buscar_id(session["id_usuario"])
    if not usuario:
        session.clear()
        flash("Tu sesión no es válida. Inicia sesión de nuevo.", "danger")
        return redirect(url_for("inicio"))

    if tarea.usuario_id != usuario.id_usuario:
        flash("No tienes permiso para modificar esta tarea.", "danger")
        return redirect(url_for("tareas"))

    datos = {
        "id_tarea": id,
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "categoria_id": request.form.get("categoria_id", "").strip(),
        "prioridad_id": request.form.get("prioridad_id", "").strip(),
        "estado_id": request.form.get("estado_id", "").strip(),
        "usuario_id": session["id_usuario"]
    }

    if not Tareas.validar_tarea(datos):
        return render_template(
            "editar_tarea.html",
            tarea=datos,
            categorias=Categorias.visualizar_todos(),
            prioridades=Prioridades.visualizar_todos(),
            estados=Estados.visualizar_todos()
        )

    Tareas.modificar(datos)
    flash("Tarea modificada exitosamente.", "success")
    return redirect(url_for("tareas"))


@app.route("/tareas/eliminar/<int:id>", methods=["POST"])
def tarea_eliminar(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder eliminar una tarea.", "danger")
        return redirect(url_for("tareas"))

    tarea = Tareas.buscar_id(id)
    if not tarea:
        flash("Ups, parece que la tarea ya no existe...", "danger")
        return redirect(url_for("tareas"))

    usuario = Usuarios.buscar_id(session["id_usuario"])
    if not usuario:
        session.clear()
        flash("Tu sesión no es válida. Inicia sesión de nuevo.", "danger")
        return redirect(url_for("inicio"))

    if tarea.usuario_id != usuario.id_usuario:
        flash("No tienes permiso para eliminar esta tarea.", "danger")
        return redirect(url_for("tareas"))

    Tareas.eliminar(id)
    flash("Tarea eliminada correctamente.", "success")
    return redirect(url_for("tareas"))