from flask import Blueprint, request, jsonify, url_for
from src.core import empleados
from flask import render_template , flash, redirect
from src.core.auth.decorators import login_required, check
from src.web.validators.empleado_validadores import validate_empleado_form


bp = Blueprint('empleados', __name__, url_prefix="/empleados", template_folder='../templates/empleados',static_folder="/admin/static")

@bp.get("/")
@login_required
@check("team_index")
def index():
    """
    Muestra la lista de empleados con filtros y ordenación.
    """
    nombre = request.args.get('nombre', '').strip()
    apellido = request.args.get('apellido', '').strip()
    dni = request.args.get('dni', '').strip()
    email = request.args.get('email', '').strip()
    puesto = request.args.get('puesto', '').strip() 
    sort_by = request.args.get('sort_by', 'nombre')
    order = request.args.get('order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    empleados_pagination = empleados.search_empleados(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        email=email,
        puesto=puesto,
        sort_by=sort_by,
        order=order,
        page=page,
        per_page=per_page
    )

    return render_template(
        "empleados/index_empleados.html",
        empleados=empleados_pagination.items,
        pagination=empleados_pagination,
    )


@bp.get("/crear_empleado")
@login_required
@check("team_new")
def show_create_employee_form():
    """
    Muestra el formulario para crear un nuevo empleado.

    Returns:
        Renderizado de la plantilla crear_empleado.html.
    """
    return render_template("empleados/crear_empleado.html")


@bp.post("/crear_empleado")
@login_required
@check("team_new")
def crear_empleado_listo():
    empleado_data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "dni": request.form['dni'],
        "domicilio": request.form['domicilio'],
        "email": request.form['email'],
        "localidad": request.form['localidad'],
        "telefono": request.form['telefono'],
        "profesion": request.form['profesion'],
        "puesto": request.form['puesto'],
        "fecha_inicio": request.form['fecha_inicio'],
        "contacto_emergencia": request.form['contacto_emergencia'],
        "obra_social": request.form.get('obra_social'),
        "numero_afiliado": request.form.get('numero_afiliado'),
        "condicion": request.form['condicion'],
        "activo": True if request.form['activo'] == 'true' else False
    }
    
    if request.form.get('fecha_cese'):
        empleado_data["fecha_cese"] = request.form.get('fecha_cese')

    errores = validate_empleado_form(empleado_data)
    if errores:
        flash("Ocurrió un error al completar los campos, intente nuevamente...", "danger")
        for error in errores:
            flash(error, "error")
        return redirect(url_for('empleados.show_create_employee_form'))
    
    empleado = empleados.crear_empleado(**empleado_data)
    if not empleado:
        flash("El empleado ya existe o ocurrió un error", "danger")
        return  redirect(url_for('empleados.show_create_employee_form'))
    
    flash("Empleado creado exitosamente", "success")
    return redirect("/empleados")

@bp.get("/actualizar/<int:empleado_dni>")
@login_required
@check("team_update")
def show_update_employee_form(empleado_dni):
    """
    Muestra el formulario de actualización para un empleado específico.
    
    Args:
        empleado_dni: DNI del empleado a actualizar.
    
    Returns:
        Renderizado de la plantilla update_empleado.html con los datos del empleado.
    """
    empleado = empleados.get_empleado_por_dni(empleado_dni)
    if not empleado:
        flash("Empleado no encontrado", "danger")
        return redirect("/empleados")
    
    return render_template("empleados/update_empleado.html", empleado=empleado)


@bp.post("/actualizar/<int:empleado_dni>/<int:empleado_id>")

@login_required
@check("team_update")
def update_employee(empleado_dni, empleado_id):
    """
    Actualiza los datos de un empleado existente.
    Valida y procesa los datos del formulario de actualización.
    
    Args:
        empleado_dni: DNI del empleado a actualizar.
    
    Returns:
        Redirige a la vista principal de empleados o muestra errores en caso de fallos.
    """
    empleado_data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "dni": request.form['dni'],
        "domicilio": request.form['domicilio'],
        "email": request.form["email"],
        "localidad": request.form["localidad"],
        "telefono": request.form["telefono"],
        "profesion": request.form["profesion"],
        "puesto": request.form["puesto"],
        "fecha_inicio": request.form["fecha_inicio"],
        "contacto_emergencia": request.form["contacto_emergencia"],
        "obra_social": request.form["obra_social"],
        "numero_afiliado": request.form["numero_afiliado"],
        "condicion": request.form["condicion"],
        "activo": request.form["activo"] == "true",
        "estado": True
    }

    if request.form.get('fecha_cese'):
        empleado_data["fecha_cese"] = request.form.get('fecha_cese')
        
    errores = validate_empleado_form(empleado_data)
    print(errores)
    if errores:
        flash("Ocurrió un error al completar los campos, intente nuevamente...", "danger")
        return redirect(f"/empleados/actualizar/{empleado_dni}")
    
    result = empleados.actualizar_empleado(empleado_id, **empleado_data)
    if not result:
        flash("El empleado ya existe u ocurrió un error", "danger")
        return redirect(f"/empleados/actualizar/{empleado_dni}")
    
    flash("Empleado actualizado exitosamente", "success")
    return redirect("/empleados")

@bp.post("/eliminar/<int:empleado_dni>")
@login_required
@check("team_destroy")
def delete_employee(empleado_dni):
    """
    Elimina un empleado de la base de datos.
    
    Args:
        empleado_dni: DNI del empleado a eliminar.
    
    Returns:
        Redirige a la vista principal de empleados después de eliminar al empleado.
    """
    empleados.eliminar_empleado(empleado_dni)
    flash("Empleado eliminado exitosamente", "success")
    return redirect("/empleados")

@bp.get("/detalle/<int:empleado_dni>")
@login_required
@check("team_show")
def show_empleado(empleado_dni):
    """
    Muestra el formulario para crear un nuevo empleado.

    Returns:
        Renderizado de la plantilla crear_empleado.html.
    """
    empleado = empleados.get_empleado_por_dni(empleado_dni)
    return render_template("empleados/detalles_empleado.html", empleado=empleado)
