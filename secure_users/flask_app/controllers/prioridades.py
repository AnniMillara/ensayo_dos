from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.usuario import Usuarios
from flask_app.models.prioridad import Prioridades
from flask_app.models.tarea import Tareas


@app.route("/prioridades")
def lista_prioridades():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    prioridades = Prioridades.visualizar_todos()
    return render_template("prioridades.html", prioridades=prioridades)


@app.route("/prioridades/nueva")
def nueva_prioridad():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    return render_template("nueva_prioridad.html")


@app.route("/prioridades/crear", methods=["POST"])
def crear_prioridad():
    if "id_usuario" not in session:
        flash("Inicia sesión para poder ingresar una prioridad.", "danger")
        return redirect(url_for("lista_prioridades"))

    usuario = Usuarios.buscar_id(session["id_usuario"])
    if not usuario:
        session.clear()
        flash("Tu sesión ya no es válida. Inicia sesión de nuevo.", "danger")
        return redirect(url_for("inicio"))

    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()

    if not nombre or not descripcion:
        flash("Todos los campos son obligatorios.", "danger")
        return render_template(
            "nueva_prioridad.html",
            datos={"nombre": nombre, "descripcion": descripcion}
        )

    datos = {"nombre": nombre, "descripcion": descripcion}

    Prioridades.guardar(datos)
    flash("Prioridad guardada correctamente.", "success")
    return redirect(url_for("lista_prioridades"))


@app.route("/prioridades/editar/<int:id>")
def editar_prioridad(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    prioridad = Prioridades.buscar_id(id)
    if not prioridad:
        flash("La prioridad no existe.", "danger")
        return redirect(url_for("lista_prioridades"))

    return render_template("editar_prioridad.html", prioridad=prioridad)


@app.route("/prioridades/modificar/<int:id>", methods=["POST"])
def modificar_prioridad(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    prioridad = Prioridades.buscar_id(id)
    if not prioridad:
        flash("La prioridad no existe.", "danger")
        return redirect(url_for("lista_prioridades"))

    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()

    if not nombre or not descripcion:
        flash("Todos los campos son obligatorios.", "danger")
        return render_template(
            "editar_prioridad.html",
            prioridad={"id_prioridad": id, "nombre": nombre, "descripcion": descripcion}
        )

    datos = {"id_prioridad": id, "nombre": nombre, "descripcion": descripcion}

    Prioridades.modificar(datos)
    flash("Prioridad modificada correctamente.", "success")
    return redirect(url_for("lista_prioridades"))


@app.route("/prioridades/eliminar/<int:id>", methods=["POST"])
def prioridad_eliminar(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder eliminar una prioridad.", "danger")
        return redirect(url_for("lista_prioridades"))

    prioridad = Prioridades.buscar_id(id)
    if not prioridad:
        flash("Ups, parece que ya no existe...", "danger")
        return redirect(url_for("lista_prioridades"))

    tareas = Tareas.buscar_prioridad(prioridad.id_prioridad)
    if tareas:
        flash("No puedes eliminar esta prioridad porque tiene tareas asociadas.", "danger")
        return redirect(url_for("lista_prioridades"))

    Prioridades.eliminar(id)
    flash("Prioridad eliminada correctamente.", "success")
    return redirect(url_for("lista_prioridades"))