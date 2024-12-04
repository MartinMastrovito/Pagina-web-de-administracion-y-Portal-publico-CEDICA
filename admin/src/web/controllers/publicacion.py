from flask import render_template, request, Blueprint, flash, redirect
from flask_ckeditor.utils import cleanify
from src.core import publicacion
from src.core.empleados import get_empleados, get_empleado_by_id
from src.core.auth.decorators import login_required, check
from datetime import datetime, timezone

bp = Blueprint("publicacion", __name__, url_prefix="/publicacion")

@bp.get("/")
@login_required
@check("publicacion_index")
def index():
    """
    Muestra la lista de publicaciones con paginación.

    Obtiene las publicaciones de la base de datos y las muestra en una página de listado.
    La paginación se maneja mediante los parámetros `page` y `per_page`.

    Returns:
        render_template: Devuelve la plantilla renderizada con la lista de publicaciones.
    """
    page = request.args.get("page", 1, type=int)
    per_page = 10
    estado = request.args.get('estado', '', type=str)
    sort_by = request.args.get("orden", "fecha_actualizacion")
    order = request.args.get("order", "desc")
    publicaciones = publicacion.obtener_publicaciones(estado, sort_by, order, page, per_page)
    
    return render_template(
        "publicaciones/listar.html", 
        publicaciones=publicaciones.items,
        pagination=publicaciones,
        estado=estado,
        sort_by=sort_by,
        order=order,
    )

@bp.get("/crear")
@login_required
@check("publicacion_new")
def show_crear_publicacion():
    """
    Muestra el formulario para crear una nueva publicación.

    Obtiene la lista de empleados para mostrarla en el formulario de creación.

    Returns:
        render_template: Devuelve la plantilla con el formulario de creación de la publicación.
    """
    empleados = get_empleados()
    return render_template("publicaciones/crear_publicacion.html", empleados=empleados)

@bp.post("/crear")
@login_required
@check("publicacion_new")
def crear_publicacion():
    """
    Crea una nueva publicación y la guarda en la base de datos.

    Obtiene los datos del formulario y, si el estado de la publicación es 'Publicado',
    se asigna la fecha de publicación. Luego, la publicación se guarda en la base de datos.

    Returns:
        redirect: Redirige al listado de publicaciones con un mensaje de éxito.
    """
    pub_data = {
        "titulo": request.form["titulo"],
        "copete": request.form["copete"],
        "contenido": cleanify(request.form.get('ckeditor')),
        "autor_id": request.form["autor_id"],
        "estado": request.form["estado"],
        "fecha_publicacion": datetime.now(timezone.utc) if request.form["estado"] == "Publicado" else None,
        "fecha_creacion": datetime.now(timezone.utc),
        "fecha_actualizacion": datetime.now(timezone.utc),
    }
    
    empleado = get_empleado_by_id(pub_data["autor_id"])
    pub_data["nombre_autor"] = f"{empleado.nombre} {empleado.apellido}"
    
    publicacion.crear_publicacion(pub_data)
    flash("Publicacion creada correctamente", "success")
    return redirect("/publicacion")

@bp.post("/eliminar/<int:id>")
@login_required
@check("publicacion_delete")
def eliminar_publicacion(id):
    """
    Elimina una publicación por su ID.

    Busca la publicación por su ID y la elimina de la base de datos.

    Args:
        id: El ID de la publicación a eliminar.

    Returns:
        redirect: Redirige al listado de publicaciones con un mensaje de éxito.
    """
    publicacion.eliminar_publicacion(id)
    flash("Publicacion eliminada correctamente", "success")
    return redirect("/publicacion")

@bp.get("/actualizar/<int:id>")
@login_required
@check("publicacion_update")
def show_actualizar_publicacion(id):
    """
    Muestra el formulario para actualizar una publicación existente.

    Obtiene la publicación por su ID y la lista de empleados, para mostrarla en el formulario
    de actualización.

    Args:
        id : El ID de la publicación a actualizar.

    Returns:
        render_template: Devuelve la plantilla con el formulario de actualización de la publicación.
    """
    empleados = get_empleados()
    pub = publicacion.get_publicacion(id)
    return render_template("publicaciones/actualizar_publicacion.html", empleados=empleados, publicacion=pub)

@bp.post("/actualizar/<int:id>")
@login_required
@check("publicacion_update")
def actualizar_publicacion(id):
    """
    Actualiza una publicación existente en la base de datos.

    Obtiene los datos del formulario y, si el estado de la publicación es 'Publicado',
    se asigna la fecha de publicación. Luego, actualiza la publicación en la base de datos.

    Args:
        id : El ID de la publicación a actualizar.

    Returns:
        redirect: Redirige al listado de publicaciones con un mensaje de éxito.
    """
    pub_data = {
        "titulo": request.form["titulo"],
        "copete": request.form["copete"],
        "contenido": cleanify(request.form.get('ckeditor')),
        "autor_id": request.form["autor_id"],
        "estado": request.form["estado"],
        "fecha_publicacion": datetime.now(timezone.utc) if request.form["estado"] == "Publicado" else None,
        "fecha_actualizacion": datetime.now(timezone.utc),
    }
    
    publicacion.actualizar_publicacion(id, **pub_data)
    flash("Publicacion actualizada correctamente", "success")
    return redirect("/publicacion")

@bp.get("/detalles/<int:id>")
@login_required
@check("publicacion_show")
def show_publicacion(id):
    """
    Muestra los detalles de una publicación específica.

    Obtiene la publicación por su ID y la muestra en una plantilla de detalles.

    Args:
        id : El ID de la publicación a mostrar.

    Returns:
        render_template: Devuelve la plantilla con los detalles de la publicación.
    """
    pub = publicacion.get_publicacion(id)
    return render_template("publicaciones/show_publicacion.html", pub=pub)