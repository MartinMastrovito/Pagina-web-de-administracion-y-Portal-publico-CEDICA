from flask import Blueprint, request, jsonify, url_for
from src.core import empleados
from flask import render_template , flash, redirect, current_app
from src.core.auth.decorators import login_required, check
from src.web.validators.empleado_validadores import validate_empleado_form


empleados_bp = Blueprint('empleados', __name__, url_prefix="/menu_empleados", template_folder='../templates/empleados',static_folder="/admin/static")

@empleados_bp.get("/menu")
def show_empleado_form():
    return render_template("empleados/menu_empleados.html")

#crear empleados

@empleados_bp.get("/crear")
def show_create_employee_form():
    """
    Muestra el formulario para crear un nuevo empleado.

    Returns:
        Renderizado de la plantilla crear_empleado.html.
    """
    return render_template("empleados/crear_empleado.html")


@empleados_bp.post("/crear_empleado")
#@login_required
def crear_empleado_listo():
    # Obtener los datos del formulario
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
        "fecha_cese": request.form.get('fecha_cese'),  # Puede ser None si no se proporciona
        "contacto_emergencia": request.form['contacto_emergencia'],
        "obra_social": request.form.get('obra_social'),  # Opcional
        "numero_afiliado": request.form.get('numero_afiliado'),  # Opcional
        "condicion": request.form['condicion'],
        "activo": True if request.form['activo'] == 'true' else False
    }

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
    return redirect(url_for('empleados.listar_empleados'))



# listar empleados
@empleados_bp.route('/lista-empleados', methods=['GET'])

def listar_empleados():
    """
    Renderiza la vista principal de empleados con los registros paginados.
    Se pueden filtrar resultados por nombre, apellido, dni y puesto.

    Returns:
        Renderizado de la plantilla listar_empleados.html con los resultados y la paginación.
    """
    nombre = request.args.get("nombre")
    apellido = request.args.get("apellido")
    dni = request.args.get("dni", type=int)
    puesto = request.args.get("puesto")
    sort_by = request.args.get("sort_by", "nombre")
    order = request.args.get("order", "asc")
    page = request.args.get("page", 1, type=int)
    per_page = 25

    empleados_paginacion = empleados.buscar_empleado(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        puesto=puesto,
        sort_by=sort_by,
        order=order,
        page=page,
        per_page=per_page
    )

    return render_template(
        "empleados/listar_empleados.html",
        empleados=empleados_paginacion.items,
        paginacion=empleados_paginacion
    )

# actualizar empleados

@empleados_bp.get("/actualizar/<int:empleado_dni>")
@login_required
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


@empleados_bp.post("/actualizar/<int:empleado_dni>")
@login_required
def update_employee(empleado_dni):
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
        "profesión": request.form["profesión"],
        "puesto": request.form["puesto"],
        "fecha_inicio": request.form["fecha_inicio"],
        "fecha_cese": request.form["fecha_cese"],
        "contacto_emergencia": request.form["contacto_emergencia"],
        "obra_social": request.form["obra_social"],
        "numero_afiliado": request.form["numero_afiliado"],
        "condicion": request.form["condicion"],
        "activo": request.form["activo"],
    }

    errores = validate_empleado_form(empleado_data)
    if errores:
        flash("Ocurrió un error al completar los campos, intente nuevamente...", "danger")
        return redirect(f"/empleados/actualizar/{empleado_dni}")
    
    result = empleados.update_employee(empleado_dni, **empleado_data)
    if not result:
        flash("El empleado ya existe o ocurrió un error", "danger")
        return redirect(f"/empleados/actualizar/{empleado_dni}")
    
    flash("Empleado actualizado exitosamente", "success")
    return redirect("/empleados")


# eliminar empleados

@empleados_bp.get("menu_empleados/eliminar/<int:empleado_dni>")
@login_required
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

