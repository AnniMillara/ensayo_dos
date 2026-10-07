from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.usuario import Usuarios
from flask_app.models.categoria import Categorias
from flask_app.models.tarea import Tareas


@app.route("/categorias")
def lista_categorias():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    categorias = Categorias.visualizar_todos()
    return render_template("categorias.html", categorias=categorias)


@app.route("/categorias/nueva")
def nueva_categoria():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    return render_template("nueva_categoria.html")


@app.route("/categorias/crear", methods=["POST"])
def crear_categoria():
    if "id_usuario" not in session:
        flash("Inicia sesión para poder ingresar una categoría.", "danger")
        return redirect(url_for("lista_categorias"))

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
            "nueva_categoria.html",
            datos={"nombre": nombre, "descripcion": descripcion}
        )

    datos = {"nombre": nombre, "descripcion": descripcion}

    Categorias.guardar(datos)
    flash("Categoría guardada correctamente.", "success")
    return redirect(url_for("lista_categorias"))


@app.route("/categorias/editar/<int:id>")
def editar_categoria(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    categoria = Categorias.buscar_id(id)
    if not categoria:
        flash("La categoría no existe.", "danger")
        return redirect(url_for("lista_categorias"))

    return render_template("editar_categoria.html", categoria=categoria)


@app.route("/categorias/modificar/<int:id>", methods=["POST"])
def modificar_categoria(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    categoria = Categorias.buscar_id(id)
    if not categoria:
        flash("La categoría no existe.", "danger")
        return redirect(url_for("lista_categorias"))

    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()

    if not nombre or not descripcion:
        flash("Todos los campos son obligatorios.", "danger")
        return render_template(
            "editar_categoria.html",
            categoria={"id_categoria": id, "nombre": nombre, "descripcion": descripcion}
        )

    datos = {"id_categoria": id, "nombre": nombre, "descripcion": descripcion}

    Categorias.modificar(datos)
    flash("Categoría modificada correctamente.", "success")
    return redirect(url_for("lista_categorias"))


@app.route("/categorias/eliminar/<int:id>", methods=["POST"])
def categoria_eliminar(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder eliminar esta categoría.", "danger")
        return redirect(url_for("lista_categorias"))

    categoria = Categorias.buscar_id(id)
    if not categoria:
        flash("Ups, parece que ya no existe...", "danger")
        return redirect(url_for("lista_categorias"))

    tareas = Tareas.buscar_categoria(categoria.id_categoria)
    if tareas:
        flash("No puedes eliminar esta categoría porque tiene tareas asociadas.", "danger")
        return redirect(url_for("lista_categorias"))

    Categorias.eliminar(id)
    flash("Categoría eliminada correctamente.", "success")
    return redirect(url_for("lista_categorias"))