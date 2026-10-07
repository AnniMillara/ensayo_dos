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

    usuario_id = session["id_usuario"]

    # Filtros (GET)
    buscar = request.args.get("buscar", "").strip().lower()
    filtro_categoria = request.args.get("categoria_id", "").strip()
    filtro_estado = request.args.get("estado_id", "").strip()

    todas = Tareas.visualizar_todos()

    # Filtrar solo las del usuario actual
    todas = [t for t in todas if t.usuario_id == usuario_id]

    if buscar:
        todas = [t for t in todas if buscar in t.nombre.lower()]
    if filtro_categoria:
        todas = [t for t in todas if str(t.categoria_id) == filtro_categoria]
    if filtro_estado:
        todas = [t for t in todas if str(t.estado_id) == filtro_estado]

    # Próximas tareas (top 5)
    proximas = Tareas.proximas(usuario_id, 5)

    # Resumen
    conteo = Tareas.contar_por_estado(usuario_id)
    resumen = {"total": 0, "pendientes": 0, "en_progreso": 0, "completadas": 0}
    for fila in conteo:
        resumen["total"] += fila["total"]
        nombre = fila["estado"].lower()
        if "pendiente" in nombre:
            resumen["pendientes"] = fila["total"]
        elif "progreso" in nombre:
            resumen["en_progreso"] = fila["total"]
        elif "complet" in nombre:
            resumen["completadas"] = fila["total"]

    return render_template(
        "tareas.html",
        tareas=todas,
        categorias=Categorias.visualizar_todos(),
        estados=Estados.visualizar_todos(),
        proximas=proximas,
        resumen=resumen,
        filtros={"buscar": buscar, "categoria_id": filtro_categoria, "estado_id": filtro_estado}
    )


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
    return render_template("tarea_detalle.html", tarea=tarea, comentarios=comentarios)


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
        flash("Tu sesión ya no es válida.", "danger")
        return redirect(url_for("inicio"))

    datos = {
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "fecha_limite": request.form.get("fecha_limite", "").strip(),
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
        flash("Tu sesión no es válida.", "danger")
        return redirect(url_for("inicio"))

    if tarea.usuario_id != usuario.id_usuario:
        flash("No tienes permiso para modificar esta tarea.", "danger")
        return redirect(url_for("tareas"))

    datos = {
        "id_tarea": id,
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "fecha_limite": request.form.get("fecha_limite", "").strip(),
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
        flash("Tu sesión no es válida.", "danger")
        return redirect(url_for("inicio"))

    if tarea.usuario_id != usuario.id_usuario:
        flash("No tienes permiso para eliminar esta tarea.", "danger")
        return redirect(url_for("tareas"))

    Tareas.eliminar(id)
    flash("Tarea eliminada correctamente.", "success")
    return redirect(url_for("tareas"))


@app.route("/tareas/completar/<int:id>", methods=["POST"])
def completar_tarea(id):
    """Marca la tarea como completada cambiando su estado al estado 'Completada'."""
    if "id_usuario" not in session:
        flash("Inicia sesión.", "danger")
        return redirect(url_for("inicio"))

    tarea = Tareas.buscar_id(id)
    if not tarea or tarea.usuario_id != session["id_usuario"]:
        flash("No tienes permiso.", "danger")
        return redirect(url_for("tareas"))

    # Buscar el estado que contenga "complet"
    estados = Estados.visualizar_todos()
    estado_completado = next((e for e in estados if "complet" in e.nombre.lower()), None)
    if not estado_completado:
        flash("No existe un estado 'Completada'.", "danger")
        return redirect(url_for("detalle_tarea", id=id))

    datos = {
        "id_tarea": id,
        "nombre": tarea.nombre,
        "descripcion": tarea.descripcion,
        "fecha_limite": tarea.fecha_limite,
        "categoria_id": tarea.categoria_id,
        "prioridad_id": tarea.prioridad_id,
        "estado_id": estado_completado.id_estado
    }

    Tareas.modificar(datos)
    flash("Tarea marcada como completada.", "success")
    return redirect(url_for("detalle_tarea", id=id))