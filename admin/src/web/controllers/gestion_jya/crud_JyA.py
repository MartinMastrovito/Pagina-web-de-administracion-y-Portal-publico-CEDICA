from flask import render_template, request, redirect, flash, Blueprint
from src.core import crud_JyA
from src.core.auth.decorators import login_required, check
from src.web.validators.jya_validations import validate_jya_form

bp = Blueprint("crud_JyA", __name__, url_prefix="/JYA")

@bp.get("/")
@login_required
@check("jya_index")
def index():
    """
    Renderiza la vista principal de JYA con los registros paginados de usuarios.
    Se pueden filtrar resultados por nombre, apellido, dni y profesionales atendiendo.

    Returns:
        Renderizado de la plantilla list_jya.html con los resultados y la paginación.
    """
    nombre = request.args.get("nombre")
    apellido = request.args.get("apellido")
    dni = request.args.get("dni", type=int)
    profesionales_atendiendo = request.args.get("profesionales_atendiendo")
    sort_by = request.args.get("sort_by", "nombre")
    order = request.args.get("order", "asc")
    page = request.args.get("page", 1, type=int)
    per_page = 10

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

    return render_template(
        "JYA/list_jya.html",
        jyas=users_pagination.items,
        pagination=users_pagination
    )
    
@bp.get("/crear_jya")
@login_required
@check("jya_new")
def show_create_jya_form():
    """
    Muestra el formulario para crear un nuevo JYA.
    Verifica la existencia de empleados y caballos necesarios para la creación.

    Returns:
        Renderizado de la plantilla create_jya.html si existen los recursos requeridos,
        de lo contrario redirige a la vista principal.
    """
    empleados_terapeuta_profesor = crud_JyA.get_empleados_terapeuta_profesor()
    empleados_conductor = crud_JyA.get_empleados_conductor()
    empleados_auxiliar = crud_JyA.get_empleados_auxiliar()
    caballos = crud_JyA.get_caballos()

    if not (empleados_terapeuta_profesor and empleados_conductor and empleados_auxiliar and caballos):
        flash(
            "Debe asegurarse de que exista por lo menos un empleado terapeuta/profesor, "
            "conductor, auxiliar de pista y un caballo en el sistema",
            "danger"
        )
        return redirect("/JYA")

    return render_template(
        "JYA/create_jya.html",
        empleados_terapeuta_profesor=empleados_terapeuta_profesor,
        empleados_conductor=empleados_conductor,
        empleados_auxiliar=empleados_auxiliar,
        caballos=caballos
    )

@bp.post("/crear_jya")
@login_required
@check("jya_new")
def create_jya():
    """
    Crea un nuevo JYA con los datos proporcionados por el formulario.
    Valida los datos ingresados y redirige a la lista de JYA o muestra errores en caso de fallos.

    Returns:
        Redirige a la lista de JYA o a la vista de creación en caso de errores.
    """
    jya_data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "dni": request.form['dni'],
        "edad": request.form["edad"],
        "fecha_nacimiento": request.form["fecha_nacimiento"],
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
        "observaciones_beca": request.form["observaciones_beca"],
        "profesionales_atendiendo": request.form["profesionales_atendiendo"],
        "certificado_discapacidad": request.form["certificado_discapacidad"] == "true",
        "tipo_discapacidad": request.form.get("tipo_discapacidad", None),
        "asignacion_familiar": request.form["asignacion_familiar"] == "true",
        "tipo_asignacion": request.form.get("tipo_asignacion", ""),
        "pension": request.form["pension"] == "true",
        "tipo_pension": request.form.get("tipo_pension", ""),
        "obra_social": request.form.get("obra_social", ""),
        "numero_afiliado": request.form.get("numero_afiliado", ""),
        "curatela": request.form["curatela"] == "true",
        "observaciones_previsionales": request.form.get("observaciones_previsionales", ""),
        "institucion_escolar": {
            "nombre": request.form["institucion_escolar_nombre"],
            "direccion": request.form["institucion_escolar_direccion"],
            "telefono": request.form["institucion_escolar_telefono"],
            "grado_actual": request.form["grado_actual"],
            "observaciones": request.form.get("institucion_escolar_observaciones", "")
        },
        "familiares_tutores": [],
        "propuesta_trabajo": request.form["propuesta_trabajo"],
        "condicion_trabajo": request.form["condicion_trabajo"],
        "sede": request.form["sede"],
        "dias_asistencia": request.form.getlist("dias_asistencia"),
    }
    
    if request.form.get("diagnostico_discapacidad", "") == "OTRO":
        jya_data["diagnostico_discapacidad"] = request.form.get("otro_diagnostico", "")
    else:
        jya_data["diagnostico_discapacidad"] = request.form.get("diagnostico_discapacidad", "")

    if 'familiar1_parentesco' in request.form:
        jya_data["familiares_tutores"].append({
            "parentesco": request.form.get("familiar1_parentesco", ""),
            "nombre": request.form.get("familiar1_nombre", ""),
            "apellido": request.form.get("familiar1_apellido", ""),
            "dni": request.form.get("familiar1_dni", ""),
            "domicilio_actual": request.form.get("familiar1_domicilio_actual", ""),
            "celular_actual": request.form.get("familiar1_celular_actual", ""),
            "email": request.form.get("familiar1_email", ""),
            "nivel_escolaridad": request.form.get("familiar1_nivel_escolaridad", ""),
            "ocupacion": request.form.get("familiar1_ocupacion", "")
        })

    if 'familiar2_parentesco' in request.form:
        jya_data["familiares_tutores"].append({
            "parentesco": request.form.get("familiar2_parentesco", ""),
            "nombre": request.form.get("familiar2_nombre", ""),
            "apellido": request.form.get("familiar2_apellido", ""),
            "dni": request.form.get("familiar2_dni", ""),
            "domicilio_actual": request.form.get("familiar2_domicilio_actual", ""),
            "celular_actual": request.form.get("familiar2_celular_actual", ""),
            "email": request.form.get("familiar2_email", ""),
            "nivel_escolaridad": request.form.get("familiar2_nivel_escolaridad", ""),
            "ocupacion": request.form.get("familiar2_ocupacion", "")
        })

    errores = validate_jya_form(jya_data)
    if errores:
        flash("Ocurrió un error al completar los campos, intentelo nuevamente...", "danger")
        return redirect("/JYA/crear_jya")
    
    user = crud_JyA.create_jya(request.form["caballo_id"], **jya_data)
    if not user:
        flash("El usuario ya existe u ocurrió un error", "danger")
        return redirect("/JYA/crear_jya")
    
    crud_JyA.assign_employee_to_jya(user.id, request.form["profesor_terapeuta_id"], "terapeuta")
    crud_JyA.assign_employee_to_jya(user.id, request.form["conductor_caballo_id"], "conductor")
    crud_JyA.assign_employee_to_jya(user.id, request.form["auxiliar_id"], "auxiliar")

    flash("JYA creado exitosamente", "success")
    return redirect("/JYA")
    
@bp.get("/actualizar/<int:jya_dni>")
@login_required
@check("jya_update")
def show_update_jya(jya_dni):
    """
    Muestra el formulario de actualización para un JYA específico.
    
    Args:
        jya_dni: DNI del JYA a actualizar.
    
    Returns:
        Renderizado de la plantilla update_jya.html con los datos del JYA.
    """
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    empleados_jya = crud_JyA.get_jyaempleados_id(jya)
    
    empleados_terapeuta_profesor = crud_JyA.get_empleados_terapeuta_profesor()
    empleados_conductor = crud_JyA.get_empleados_conductor()
    empleados_auxiliar = crud_JyA.get_empleados_auxiliar()
    caballos = crud_JyA.get_caballos()

    if not (empleados_terapeuta_profesor and empleados_conductor and empleados_auxiliar and caballos):
        flash(
            "Debe asegurarse de que exista por lo menos un empleado terapeuta/profesor, "
            "conductor, auxiliar de pista y un caballo en el sistema",
            "danger"
        )
        return redirect(f"/JYA/detalles/{jya_dni}")
    
    return render_template(
        "JYA/update_jya.html",
        jya=jya,
        empleados_terapeuta_profesor=empleados_terapeuta_profesor,
        empleados_conductor=empleados_conductor,
        empleados_auxiliar=empleados_auxiliar,
        caballos=caballos,
        empleados_jya=empleados_jya,
    )

@bp.post("/actualizar/<int:jya_dni>")
@login_required
@check("jya_update")
def jya_update(jya_dni):
    """
    Actualiza los datos de un JYA existente.
    Valida y procesa los datos del formulario de actualización.
    
    Args:
        jya_dni: DNI del JYA a actualizar.
    
    Returns:
        Redirige a la vista principal de JYA o muestra errores en caso de fallos.
    """
    jya_data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "dni": request.form['dni'],
        "edad": request.form["edad"],
        "fecha_nacimiento": request.form["fecha_nacimiento"],
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
        "observaciones_beca": request.form["observaciones_beca"],
        "profesionales_atendiendo": request.form["profesionales_atendiendo"],
        "certificado_discapacidad": request.form["certificado_discapacidad"] == "true",
        "tipo_discapacidad": request.form.get("tipo_discapacidad", None),
        "asignacion_familiar": request.form["asignacion_familiar"] == "true",
        "tipo_asignacion": request.form.get("tipo_asignacion", ""),
        "pension": request.form["pension"] == "true",
        "tipo_pension": request.form.get("tipo_pension", ""),
        "obra_social": request.form.get("obra_social", ""),
        "numero_afiliado": request.form.get("numero_afiliado", ""),
        "curatela": request.form["curatela"] == "true",
        "observaciones_previsionales": request.form.get("observaciones_previsionales", ""),
        "institucion_escolar": {
            "nombre": request.form["institucion_escolar_nombre"],
            "direccion": request.form["institucion_escolar_direccion"],
            "telefono": request.form["institucion_escolar_telefono"],
            "grado_actual": request.form["grado_actual"],
            "observaciones": request.form.get("institucion_escolar_observaciones", "")
        },
        "familiares_tutores": [],
        "propuesta_trabajo": request.form["propuesta_trabajo"],
        "condicion_trabajo": request.form["condicion_trabajo"],
        "sede": request.form["sede"],
        "dias_asistencia": request.form.getlist("dias_asistencia"),
    }
        
    if request.form.get("diagnostico_discapacidad", "") == "OTRO":
        jya_data["diagnostico_discapacidad"] = request.form.get("otro_diagnostico", "")
    else:
        jya_data["diagnostico_discapacidad"] = request.form.get("diagnostico_discapacidad", "")
    
    if 'familiar1_parentesco' in request.form:
        jya_data["familiares_tutores"].append({
            "parentesco": request.form.get("familiar1_parentesco", ""),
            "nombre": request.form.get("familiar1_nombre", ""),
            "apellido": request.form.get("familiar1_apellido", ""),
            "dni": request.form.get("familiar1_dni", ""),
            "domicilio_actual": request.form.get("familiar1_domicilio_actual", ""),
            "celular_actual": request.form.get("familiar1_celular_actual", ""),
            "email": request.form.get("familiar1_email", ""),
            "nivel_escolaridad": request.form.get("familiar1_nivel_escolaridad", ""),
            "ocupacion": request.form.get("familiar1_ocupacion", "")
        })

    if 'familiar2_parentesco' in request.form:
        jya_data["familiares_tutores"].append({
            "parentesco": request.form.get("familiar2_parentesco", ""),
            "nombre": request.form.get("familiar2_nombre", ""),
            "apellido": request.form.get("familiar2_apellido", ""),
            "dni": request.form.get("familiar2_dni", ""),
            "domicilio_actual": request.form.get("familiar2_domicilio_actual", ""),
            "celular_actual": request.form.get("familiar2_celular_actual", ""),
            "email": request.form.get("familiar2_email", ""),
            "nivel_escolaridad": request.form.get("familiar2_nivel_escolaridad", ""),
            "ocupacion": request.form.get("familiar2_ocupacion", "")
        })
    
    errores = validate_jya_form(jya_data)
    if errores:
        flash("Ocurrió un error al completar los campos, intentelo nuevamente...", "danger")
        return redirect(f"/JYA/actualizar/{jya_dni}")
    
    new_unique_dni = crud_JyA.update_jya(jya_dni, request.form["caballo_id"], **jya_data)
    if new_unique_dni:
        flash("Se modificó el JYA exitosamente", "success")
        
        updated_jya = crud_JyA.get_jya_by_dni(jya_data['dni'])
        crud_JyA.assign_employee_to_jya(updated_jya.id, request.form["profesor_terapeuta_id"], "terapeuta")
        crud_JyA.assign_employee_to_jya(updated_jya.id, request.form["conductor_caballo_id"], "conductor")
        crud_JyA.assign_employee_to_jya(updated_jya.id, request.form["auxiliar_id"], "auxiliar")
        
        return redirect(f"/JYA/detalles/{updated_jya.dni}")
    else:
        flash("El DNI ingresado ya se encuentra registrado en nuestro sistema", "danger")
        return redirect(f"/JYA/actualizar/{jya_dni}")

@bp.post("/eliminar/<int:jya_dni>")
@login_required
@check("jya_destroy")
def jya_delete(jya_dni):
    """
    Elimina un JYA específico del sistema.
    
    Args:
        jya_dni: DNI del JYA a eliminar.
    
    Returns:
        Redirige a la vista principal de JYA después de la eliminación.
    """
    crud_JyA.delete_jya(jya_dni)
    flash(f"El JYA con DNI {jya_dni} y todos sus documentos asociados han sido eliminados.", "success")
    return redirect("/JYA")

@bp.get("/detalles/<int:jya_dni>")
@login_required
@check("jya_show")
def show_details_jya(jya_dni):
    """
    Muestra los detalles de un JYA específico.
    
    Args:
        jya_dni: DNI del JYA a mostrar.
    
    Returns:
        Renderizado de la plantilla show_jya.html con los detalles del JYA.
    """
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    empleados_jya = crud_JyA.get_jyaempleados(jya)
    
    if not empleados_jya["terapeuta"].empleado.estado or not empleados_jya["auxiliar"].empleado.estado or not empleados_jya["conductor"].empleado.estado:
        flash(f"Hemos realizado cambios en el personal y este JYA se ve impactado. Por favor verifique su/s empleado/s eliminado/s.", "danger")
    
    if jya.caballo.dado_de_baja:
        flash(f"Su caballo ha sido dado de baja de nuestro sistema", "danger")
      
    return render_template("JYA/show_jya.html", jya=jya, empleados_jya=empleados_jya)