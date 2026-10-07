# 🐛 Errores Comunes y Correcciones — TaskTrack

Este README recopila **todos los errores** detectados durante el desarrollo del proyecto TaskTrack, con ejemplos, explicaciones y la solución aplicada. Sirve como checklist antes de cada entrega.

---

## 📑 Índice

1. [Nombres de funciones duplicados](#1-nombres-de-funciones-duplicados-entre-controladores)
2. [`url_for` apuntando a funciones inexistentes](#2-url_for-apuntando-a-funciones-que-no-existen)
3. [Falta `return` tras `flash` de error](#3-falta-return-después-de-flash-de-error)
4. [`render_template` tras error pierde datos](#4-render_template-tras-un-error-pierde-los-datos)
5. [Comparar objetos con IDs](#5-comparar-objetos-con-ids)
6. [Eliminar o modificar con GET](#6-eliminar-o-modificar-con-get)
7. [Métodos que devuelven objeto en lugar de lista](#7-métodos-que-devuelven-objeto-cuando-deberían-devolver-lista)
8. [`session.clear()` innecesario](#8-sessionclear-cuando-el-usuario-no-es-el-dueño)
9. [Tabla equivocada en SELECT](#9-tabla-equivocada-en-consultas-sql)
10. [INSERT a tabla equivocada](#10-insert-a-tabla-equivocada)
11. [`KeyError` por nombres de columnas](#11-datakey-cuando-la-columna-se-llama-distinto)
12. [SELECT incompleto respecto al `__init__`](#12-select-incompleto-respecto-al-__init__)
13. [`tarea_id` faltante en POST de comentarios](#13-tarea_id-faltante-en-post-de-comentarios)
14. [Redirigir siempre a `index.html` tras error](#14-redirigir-siempre-a-indexhtml-tras-error)
15. [`methodts` en lugar de `methods`](#15-methodts-en-lugar-de-methods)
16. [Rutas sin protección de sesión](#16-rutas-sin-protección-de-sesión)
17. [Falta de imports](#17-falta-de-imports)
18. [Mensajes de flash copiados sin adaptar](#18-mensajes-de-flash-copiados-sin-adaptar)
19. [`usuario_id` en el UPDATE de tareas](#19-usuario_id-en-el-update-de-tareas)
20. [Plurales/singulares inconsistentes en rutas](#20-pluralessingulares-inconsistentes-en-rutas)
21. [Archivos de modelo con clase mal nombrada](#21-archivos-de-modelo-con-clase-mal-nombrada)
22. [Mezclar lógica de crear y editar en la misma plantilla](#22-mezclar-lógica-de-crear-y-editar-en-la-misma-plantilla)
23. [No verificar que la tarea pertenece al usuario](#23-no-verificar-que-la-tarea-pertenece-al-usuario)
24. [Uso incorrecto de `session["id_usuario"]` vs `usuario.id_usuario`](#24-uso-incorrecto-de-sessionid_usuario-vs-usuarioid_usuario)
25. [Falta de rutas `editar` (solo tenías `modificar`)](#25-falta-de-rutas-editar-solo-tenías-modificar)
26. [No cerrar conexión MySQL / no usar `query_db` correctamente](#26-no-cerrar-conexión-mysql--no-usar-query_db-correctamente)
27. [No validar permisos de edición de comentarios](#27-no-validar-permisos-de-edición-de-comentarios)
28. [Faltaba `tarea_detalle.html` para comentarios](#28-faltaba-tarea_detallehtml-para-comentarios)
29. [Nombres de plantillas inconsistentes](#29-nombres-de-plantillas-inconsistentes)
30. [Errores tipográficos en español](#30-errores-tipográficos-en-español)

---

## 1. Nombres de funciones duplicados entre controladores

**Error:**
```python
# tareas.py
@app.route("/tareas/crear", methods=["POST"])
def crear_tarea(): ...

# prioridades.py
@app.route("/prioridades/crear", methods=["POST"])
def crear_tarea(): ...   # ❌ ¡Mismo nombre!
```

Flask lanza: `AssertionError: View function mapping is overwriting an existing endpoint function`.

**Solución:** cada función debe tener un nombre único. Usa prefijos:
- `crear_tarea`, `crear_categoria`, `crear_estado`, `crear_prioridad`.

---

## 2. `url_for` apuntando a funciones que no existen

**Error:**
```python
return redirect(url_for("prioridades"))   # ❌ no hay función "prioridades"
```

**Solución:** asegurarte de que la función exista con **ese nombre exacto**:
```python
@app.route("/prioridades")
def lista_prioridades(): ...
# ...
return redirect(url_for("lista_prioridades"))
```

---

## 3. Falta `return` después de `flash` de error

**Error:**
```python
if not nombre or not descripcion:
    flash("Campos obligatorios.", "danger")
    # ❌ sin return → sigue y guarda igual
```

**Solución:** siempre `return` tras un error:
```python
if not nombre or not descripcion:
    flash("Campos obligatorios.", "danger")
    return render_template("nueva_prioridad.html", datos=datos)
```

---

## 4. `render_template` tras un error pierde los datos

**Error:** al recargar el formulario sin pasar los datos, el usuario debe reescribir todo.

**Solución:** pasar `datos` a la plantilla y pre-cargar los inputs:
```python
return render_template("nueva_prioridad.html",
                       datos={"nombre": nombre, "descripcion": descripcion})
```

---

## 5. Comparar objetos con IDs

**Error:**
```python
if not usuario or tarea.usuario_id != usuario:   # ❌ objeto vs int
```

**Solución:**
```python
if tarea.usuario_id != usuario.id_usuario:       # ✅
```

---

## 6. Eliminar o modificar con GET

**Error:**
```python
@app.route("/tarea/eliminar/<int:id>")   # ❌ por defecto GET
```

**Solución:**
```python
@app.route("/tareas/eliminar/<int:id>", methods=["POST"])
```
Y en el HTML: `<form method="POST">` con un `<button type="submit">`.

---

## 7. Métodos que devuelven objeto cuando deberían devolver lista

**Error:**
```python
@classmethod
def buscar_categoria(cls, id):
    ...
    if resultado:
        return cls(resultado[0])   # ❌ solo devuelve la primera
    return None
```

Si hay 3 tareas con esa categoría, `if tareas:` solo detecta una, y podrías borrar la categoría con tareas huérfanas.

**Solución:** iterar y devolver lista:
```python
@classmethod
def buscar_categoria(cls, id):
    ...
    tareas = []
    for t in resultados:
        tareas.append(cls(t))
    return tareas
```

---

## 8. `session.clear()` cuando el usuario no es el dueño

**Error:** cerrar la sesión cuando otro usuario intenta modificar algo ajeno es excesivo.

**Solución:**
```python
if tarea.usuario_id != usuario.id_usuario:
    flash("No tienes permiso.", "danger")
    return redirect(url_for("tareas"))   # ✅ solo bloquea
```

Solo limpia sesión si **el usuario logueado ya no existe**.

---

## 9. Tabla equivocada en consultas SQL

**Error:**
```python
# tarea.py
query = "SELECT ... FROM usuarios"   # ❌ debería ser "FROM tareas"
```

**Solución:** revisar que el `FROM` coincida con el modelo.

---

## 10. INSERT a tabla equivocada

**Error:**
```python
# comentario.py
query = "INSERT INTO estados(...)"   # ❌ debería ser "comentarios"
```

**Solución:** copiar/pegar del archivo correcto o revisar la tabla destino.

---

## 11. `data["id_tarea"]` cuando la columna se llama distinto

**Error:**
```python
# prioridad.py
self.id_prioridad = data["id_tarea"]   # ❌ KeyError
```

**Solución:** que el nombre del key coincida con la columna del SELECT.
```python
self.id_prioridad = data["id_prioridad"]   # ✅
```

---

## 12. SELECT incompleto respecto al `__init__`

**Error:** el `__init__` requiere `estado_id` pero el SELECT no lo trae → `KeyError`.

**Solución:** listar **todas** las columnas que necesita el constructor. Ejemplo:
```python
query = """
    SELECT
        id_tarea, nombre, descripcion,
        categoria_id, prioridad_id, estado_id, usuario_id,
        created_at, updated_at
    FROM tareas
"""
```

---

## 13. `tarea_id` faltante en POST de comentarios

**Error:**
```python
datos = {"contenido": ..., "tarea_id": }   # ❌ sintaxis inválida
```

**Solución:** pasarlo por URL:
```python
@app.route("/comentario/crear/<int:tarea_id>", methods=["POST"])
def crear_comentario(tarea_id):
    ...
    datos = {"contenido": contenido, "tarea_id": tarea_id, "usuario_id": session["id_usuario"]}
```

O mediante hidden input:
```html
<input type="hidden" name="tarea_id" value="{{ tarea.id_tarea }}">
```

---

## 14. Redirigir siempre a `index.html` tras error

**Error:**
```python
if not contenido:
    return render_template("index.html")   # ❌ el usuario pierde contexto
```

**Solución:** redirigir a la vista correcta:
```python
return redirect(url_for("detalle_tarea", id=tarea_id))
```

---

## 15. `methodts` en lugar de `methods`

**Error tipográfico:**
```python
@app.route("/tareas/crear", methodts=["POST"])   # ❌
```

**Solución:** `methods` (plural, sin t extra). Lanza `TypeError` al importar.

---

## 16. Rutas sin protección de sesión

**Error:** no verificar `session["id_usuario"]` al inicio de cada ruta.

**Solución:** patrón consistente al inicio de cada controlador:
```python
if "id_usuario" not in session:
    flash("Debes iniciar sesión.", "danger")
    return redirect(url_for("inicio"))
```

---

## 17. Falta de imports

**Error:** usar `Categorias.visualizar_todos()` sin haber importado la clase.

**Solución:** al inicio del controlador:
```python
from flask_app.models.categoria import Categorias
from flask_app.models.prioridad import Prioridades
from flask_app.models.estado import Estados
from flask_app.models.comentario import Comentarios
```

---

## 18. Mensajes de flash copiados sin adaptar

**Error:**
```python
flash("Inicia sesión para poder ingresar una estado.", "danger")
```
Estás en comentarios, no en estados. Además "una estado" es incorrecto.

**Solución:** revisar cada mensaje para que corresponda al contexto:
```python
flash("Inicia sesión para poder comentar.", "danger")
```

---

## 19. `usuario_id` en el UPDATE de tareas

**Error:** incluir `usuario_id` en el `UPDATE` no tiene sentido (cambiar dueño de tarea) y además olvidabas pasarlo → `KeyError`.

**Solución:**
```python
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
```
Y no incluir `usuario_id` en `datos`.

---

## 20. Plurales/singulares inconsistentes en rutas

**Error:** `/tarea/eliminar/` vs `/tareas/...`.

**Solución:** elegir una convención y mantenerla. Recomendado: **plural** siempre:
- `/tareas`, `/categorias`, `/estados`, `/prioridades`, `/comentarios`.

---

## 21. Archivos de modelo con clase mal nombrada

**Error:** `categoria.py` tenía `class Categoria` pero su contenido era de prioridades (`FROM prioridades`).

**Solución:** que la clase, la tabla y el `__init__` sean coherentes:
```python
# categoria.py
class Categorias:
    def __init__(self, data):
        self.id_categoria = data["id_categoria"]
        ...
        FROM categorias
```

---

## 22. Mezclar lógica de crear y editar en la misma plantilla

**Error:** reutilizar `nueva_tarea.html` para editar sin distinguir.

**Solución:** usar `editar_tarea.html` (o pasar `tarea` para que el `action` del form apunte a la ruta correcta):
```html
<form action="{{ url_for('modificar_tarea', id=tarea.id_tarea) if tarea else url_for('crear_tarea') }}" method="POST">
```

---

## 23. No verificar que la tarea pertenece al usuario

**Error:** cualquier usuario logueado podía modificar/eliminar tareas ajenas.

**Solución:**
```python
if tarea.usuario_id != usuario.id_usuario:
    flash("No tienes permiso para modificar esta tarea.", "danger")
    return redirect(url_for("tareas"))
```

---

## 24. Uso incorrecto de `session["id_usuario"]` vs `usuario.id_usuario`

**Error:** comparar directamente `tarea.usuario_id != session["id_usuario"]` sin cargar el usuario (puede quedar huérfano si el usuario fue eliminado).

**Solución:** siempre cargar el usuario primero y usar `usuario.id_usuario`:
```python
usuario = Usuarios.buscar_id(session["id_usuario"])
if not usuario:
    session.clear()
    flash("Tu sesión no es válida.", "danger")
    return redirect(url_for("inicio"))
```

---

## 25. Falta de rutas `editar` (solo tenías `modificar`)

**Error:** el botón "Editar" en la tabla no tenía a dónde ir.

**Solución:** agregar la ruta GET que muestra el formulario con datos:
```python
@app.route("/tareas/editar/<int:id>")
def editar_tarea(id):
    tarea = Tareas.buscar_id(id)
    ...
    return render_template("editar_tarea.html", tarea=tarea, ...)
```

---

## 26. No cerrar conexión MySQL / no usar `query_db` correctamente

**Error:** algunos INSERT no devolvían el `id` del registro creado, lo que rompía `session["id_usuario"] = nuevo_id`.

**Solución:** `query_db` con `INSERT` debe devolver el `insert_id`. En `mysqlconnection.py`:
```python
def query_db(query, data=None):
    cursor = connection.cursor()
    cursor.execute(query, data)
    if query.strip().upper().startswith("INSERT"):
        result = cursor.lastrowid
    else:
        result = cursor.fetchall()
    connection.commit()
    cursor.close()
    return result
```

---

## 27. No validar permisos de edición de comentarios

**Error:** cualquiera podía editar/eliminar comentarios.

**Solución:**
```python
if comentario.usuario_id != usuario.id_usuario:
    flash("No tienes permiso para eliminar este comentario.", "danger")
    return redirect(url_for("detalle_tarea", id=comentario.tarea_id))
```

---

## 28. Faltaba `tarea_detalle.html` para comentarios

**Error:** no existía la plantilla donde mostrar la tarea + sus comentarios.

**Solución:** crear `tarea_detalle.html` que renderice:
- Datos de la tarea (nombre, categoría, prioridad, estado, fecha límite).
- Lista de comentarios con autor y fecha.
- Formulario para nuevo comentario con `action="{{ url_for('crear_comentario', tarea_id=tarea.id_tarea) }}"`.

---

## 29. Nombres de plantillas inconsistentes

**Error:** a veces `tarea.html`, a veces `tareas.html`, a veces `categoria.html`, a veces `categorias.html`.

**Solución:** usar convención clara:
- `login.html` (raíz)
- `tareas.html` (listado), `nueva_tarea.html`, `editar_tarea.html`, `tarea_detalle.html`
- `categorias.html`, `nueva_categoria.html`, `editar_categoria.html`
- `estados.html`, `nuevo_estado.html`, `editar_estado.html`
- `prioridades.html`, `nueva_prioridad.html`, `editar_prioridad.html`
- `confirmar_eliminar.html`

---

## 30. Errores tipográficos en español

**Errores frecuentes:**
- `vizualizar` → **`visualizar`**
- `metodos` → **`métodos`** (en comentarios)
- `una estado` → **`un estado`**
- `Libro guardado` → **`Tarea guardada`**
- `Categoria guardado` → **`Categoría guardada`**
- `modificar esta tarea` en contexto de eliminar → **`eliminar esta tarea`**

**Solución:** revisar todos los mensajes `flash` y textos de UI.

---

## ✅ Checklist final antes de cada entrega

- [ ] Todas las funciones tienen **nombre único**.
- [ ] Todos los `url_for("...")` apuntan a funciones **existentes**.
- [ ] Cada ruta protegida verifica `session["id_usuario"]`.
- [ ] Tras cada `flash("...", "danger")` hay un `return`.
- [ ] Los métodos `buscar_*` por FK devuelven **listas**.
- [ ] Los `SELECT` traen **todas** las columnas del `__init__`.
- [ ] Los `INSERT` apuntan a la **tabla correcta**.
- [ ] Las rutas de eliminación usan `methods=["POST"]`.
- [ ] Los mensajes de `flash` coinciden con el **contexto real**.
- [ ] Los imports están completos al inicio del archivo.
- [ ] Existen las rutas `editar` (GET) y `modificar` (POST) para cada entidad.
- [ ] Los permisos de edición/eliminación se validan por `usuario_id`.
- [ ] Las plantillas tienen nombres **consistentes** (plural/singular).
- [ ] Los textos en español están **bien escritos**.

---

## 🎯 Resumen de correcciones clave

| # | Problema | Corrección |
|---|---|---|
| 1 | `buscar_categoria/estado/prioridad` devolvían un objeto | Ahora devuelven **listas** |
| 2 | `crear_comentario` sin `tarea_id` | Va en la URL `/comentario/crear/<int:tarea_id>` |
| 3 | `eliminar_usuario` con GET | Ahora POST |
| 4 | `ruta_perfil` no existía | Agregada |
| 5 | `editar_tarea/categoria/estado/prioridad` no existían | Agregadas |
| 6 | `buscar_*` por FK rompía el check `if tareas:` | Ahora retorna lista |
| 7 | Redirección a `index.html` tras error | Ahora redirige a la vista correcta |
| 8 | Falta de return tras flash de error | Corregido |
| 9 | Nombres de funciones duplicados | Prefijos únicos |
| 10 | Mensajes de flash copiados | Adaptados al contexto |
| 11 | `usuario_id` en UPDATE de tareas | Eliminado |
| 12 | Comparación `tarea.usuario_id != usuario` | Corregido a `usuario.id_usuario` |
| 13 | Rutas GET para eliminar | Cambiadas a POST |
| 14 | Nombres de plantillas inconsistentes | Convención unificada |
| 15 | Errores tipográficos | Corregidos |

---

**Autor:** TaskTrack Dev  
**Última actualización:** 2026  
**Estado del proyecto:** ✅ Funcional alineado a las capturas de referencia