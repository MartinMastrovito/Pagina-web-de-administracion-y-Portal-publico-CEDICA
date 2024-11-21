from flask import render_template, request, Blueprint, flash, redirect, url_for
from src.core import publicacion
#from src.core.empleados import get_empleados
from src.core.auth.decorators import login_required, check
from datetime import datetime, timezone

bp = Blueprint("publicacion", __name__, url_prefix="/publicacion")

@bp.get("/")
@login_required
#@check("publicacion_index")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    publicaciones = publicacion.obtener_publicaciones(page, per_page)
    
    return render_template(
        "publicaciones/listar.html", 
        publicaciones=publicaciones.items,
        pagination=publicaciones
    )

# @bp.get("/crear")
# @login_required
# #@check("publicacion_new")
# def show_crear_publicacion():
#     empleados = get_empleados()
#     return render_template("publicaciones/crear_publicacion.html", empleados=empleados)

@bp.post("/crear")
@login_required
#@check("publicacion_new")
def crear_publicacion():
    pub_data = {
        "titulo": request.form["titulo"],
        "copete": request.form["copete"],
        "contenido": request.form["contenido"],
        "autor_id": request.form["autor_id"],
        "estado": request.form["estado"],
        "fecha_publicacion": datetime.now(timezone.utc) if request.form["estado"] == "Publicado" else None,
        "fecha_creacion": datetime.now(timezone.utc),
        "fecha_actualizacion": datetime.now(timezone.utc),
    }
    
    publicacion.crear_publicacion(pub_data)
    flash("Publicacion creada correctamente", "success")
    return redirect("/publicacion")

@bp.post("/eliminar/<int:id>")
@login_required
#@check("publicacion_delete")
def eliminar_publicacion(id):
    publicacion.eliminar_publicacion(id)
    flash("Publicacion eliminada correctamente", "success")
    return redirect("/publicacion")

# @bp.get("/actualizar/<int:id>")
# @login_required
# #@check("publicacion_update")
# def show_actualizar_publicacion(id):
#     empleados = get_empleados()
#     pub = publicacion.get_publicacion(id)
#     return render_template("publicaciones/actualizar_publicacion.html", empleados=empleados, publicacion=pub)

@bp.post("/actualizar/<int:id>")
@login_required
#@check("publicacion_update")
def actualizar_publicacion(id):
    pub_data = {
        "titulo": request.form["titulo"],
        "copete": request.form["copete"],
        "contenido": request.form["contenido"],
        "autor_id": request.form["autor_id"],
        "estado": request.form["estado"],
        "fecha_publicacion": datetime.now(timezone.utc) if request.form["estado"] == "Publicado" else None,
        "fecha_actualizacion": datetime.now(timezone.utc),
    }
    
    publicacion.actualizar_publicacion(id, **pub_data)
    flash("Publicacion actualizada correctamente", "success")
    return redirect("/publicacion")
