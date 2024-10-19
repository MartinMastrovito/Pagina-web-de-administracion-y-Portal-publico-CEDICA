from flask import render_template, request, redirect, session, flash, url_for
from flask import Blueprint
from core import crud_JyA
from core.auth.decorators import login_required  # Importamos el decorador
from core.auth.decorators import check  # Importamos el decorador

bp = Blueprint("crud_JyA", __name__, url_prefix="/JYA")

@bp.get("/")
@login_required
@check("jya_index")
def index():
    nombre = request.args.get('nombre')
    apellido = request.args.get('apellido')
    dni = request.args.get('dni', type=int)
    profesionales_atendiendo = request.args.get("profesionales_atendiendo")
    sort_by = request.args.get('sort_by', 'nombre')  # Cambié 'email' a 'nombre' para evitar errores
    order = request.args.get('order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = 25

    # Obtener resultados paginados usando la búsqueda
    users_pagination = crud_JyA.search_JYA(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        profesionales_atendiendo=profesionales_atendiendo,
        sort_by=sort_by,
        order=order,
        page=page,
        per_page=per_page
    )

    # Renderizar la plantilla con la lista de JYA y la paginación
    return render_template(
        "JYA/list_jya.html",
        jyas=users_pagination.items,  # Lista de usuarios (jya) para el template
        pagination=users_pagination    # Objeto de paginación para usar en la navegación
    )
    
@bp.get("/crear_jya")
@login_required
@check("jya_new")
def show_create_jya_form():
    return render_template("JYA/create_jya.html")

@bp.post("/crear_jya")
@login_required
@check("jya_new")
def create_jya():
    jya_data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "dni": request.form['dni'],
        "edad": request.form["edad"],
        "fecha_nacimiento": request.form["fecha_de_nacimiento"],
        "lugar_nacimiento": {
            "localidad": request.form["lugar_nacimiento_localidad"],
            "provincia": request.form["lugar_nacimiento_provincia"]
        },
        "domicilio_actual": {
            "calle": request.form["domicilio_actual_calle"],
            "numero": request.form["domicilio_actual_numero"],
            "departamento": request.form.get("domicilio_actual_departamento", ""),
            "localidad": request.form["domicilio_actual_localidad"],
            "provincia": request.form["domicilio_actual_provincia"]
        },
        "telefono_actual": request.form["telefono_actual"],
        "contacto_emergencia": {
            "nombre": request.form["contacto_emergencia_nombre"],
            "telefono": request.form["contacto_emergencia_telefono"]
        },
        "becado": request.form["becado"] == "true",
        "porcentaje_beca": float(request.form["porcentaje_beca"] or 0.0),
        "profesionales_atendiendo": request.form["profesionales_atendiendo"],
    }

    user = crud_JyA.create_jya(**jya_data)
    
    if user:
        flash('Usuario creado exitosamente', 'success')
        return redirect('/JYA')
    else:
        flash('El usuario ya existe o ocurrió un error', 'danger')
        return redirect('/JYA/crear_jya')
    
@bp.get("/actualizar/<int:jya_dni>")
@login_required
@check("jya_update")
def show_update_jya(jya_dni):
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    return render_template("JYA/update_jya.html", jya=jya)

@bp.post("/actualizar/<int:jya_dni>")
@login_required
@check("jya_update")
def jya_update(jya_dni):
    jya_data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "dni": request.form['dni'],
        "edad": request.form["edad"],
        "fecha_nacimiento": request.form["fecha_de_nacimiento"],
        "lugar_nacimiento": {
            "localidad": request.form["lugar_nacimiento_localidad"],
            "provincia": request.form["lugar_nacimiento_provincia"]
        },
        "domicilio_actual": {
            "calle": request.form["domicilio_actual_calle"],
            "numero": request.form["domicilio_actual_numero"],
            "departamento": request.form.get("domicilio_actual_departamento", ""),
            "localidad": request.form["domicilio_actual_localidad"],
            "provincia": request.form["domicilio_actual_provincia"]
        },
        "telefono_actual": request.form["telefono_actual"],
        "contacto_emergencia": {
            "nombre": request.form["contacto_emergencia_nombre"],
            "telefono": request.form["contacto_emergencia_telefono"]
        },
        "becado": request.form["becado"] == "true",
        "porcentaje_beca": float(request.form["porcentaje_beca"] or 0.0),
        "profesionales_atendiendo": request.form["profesionales_atendiendo"],
    }
    crud_JyA.update_jya(jya_dni, **jya_data)
    
    return redirect('/JYA')

@bp.get("/eliminar/<int:jya_dni>")
@login_required
@check("jya_destroy")
def show_delete_jya(jya_dni):
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    return render_template("JYA/delete_jya.html", jya=jya)

@bp.post("/eliminar/<int:jya_dni>")
@login_required
@check("jya_destroy")
def jya_delete(jya_dni):
    crud_JyA.delete_jya(jya_dni)
    return redirect('/JYA')