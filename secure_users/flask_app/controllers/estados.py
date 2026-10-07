from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.usuario import Usuarios
from flask_app.models.estado import Estados
from flask_app.models.tarea import Tareas


@app.route("/estados")
def lista_estados():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    estados = Estados.visualizar_todos()
    return render_template("estados.html", estados=estados)


@app.route("/estados/nuevo")
def nuevo_estado():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    return render_template("nuevo_estado.html")


@app.route("/estados/crear", methods=["POST"])
def crear_estado():
    if "id_usuario" not in session:
        flash("Inicia sesión para poder ingresar un estado.", "danger")
        return redirect(url_for("lista_estados"))

    usuario = Usuarios.buscar_id(session["id_usuario"])
    if not usuario:
        session.clear()
        flash("Tu sesión ya no es válida.", "danger")
        return redirect(url_for("inicio"))

    datos = {
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "color": request.form.get("color", "#6b7280").strip()
    }

    if not Estados.validar_estado(datos):
        return render_template("nuevo_estado.html", datos=datos)

    Estados.guardar(datos)
    flash("Estado guardado correctamente.", "success")
    return redirect(url_for("lista_estados"))


@app.route("/estados/editar/<int:id>")
def editar_estado(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    estado = Estados.buscar_id(id)
    if not estado:
        flash("El estado no existe.", "danger")
        return redirect(url_for("lista_estados"))

    return render_template("editar_estado.html", estado=estado)


@app.route("/estados/modificar/<int:id>", methods=["POST"])
def modificar_estado(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    estado = Estados.buscar_id(id)
    if not estado:
        flash("El estado no existe.", "danger")
        return redirect(url_for("lista_estados"))

    datos = {
        "id_estado": id,
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "color": request.form.get("color", "#6b7280").strip()
    }

    if not Estados.validar_estado(datos):
        return render_template("editar_estado.html", estado=datos)

    Estados.modificar(datos)
    flash("Estado modificado correctamente.", "success")
    return redirect(url_for("lista_estados"))


@app.route("/estados/eliminar/<int:id>", methods=["POST"])
def estado_eliminar(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder eliminar este estado.", "danger")
        return redirect(url_for("lista_estados"))

    estado = Estados.buscar_id(id)
    if not estado:
        flash("Ups, parece que ya no existe...", "danger")
        return redirect(url_for("lista_estados"))

    tareas = Tareas.buscar_estado(estado.id_estado)
    if tareas:
        flash("No puedes eliminar este estado porque tiene tareas asociadas.", "danger")
        return redirect(url_for("lista_estados"))

    Estados.eliminar(id)
    flash("Estado eliminado correctamente.", "success")
    return redirect(url_for("lista_estados"))