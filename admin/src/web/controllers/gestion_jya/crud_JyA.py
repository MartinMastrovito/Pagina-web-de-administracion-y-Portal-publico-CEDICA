from flask import render_template, request, redirect, flash, Blueprint
from src.core import crud_JyA
from src.core.auth.decorators import login_required, check
from src.web.validators.jya_validations import validate_jya_form

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
    empleados_terapeuta_profesor = crud_JyA.get_empleados_terapeuta_profesor()
    empleados_conductor = crud_JyA.get_empleados_conductor()
    empleados_auxiliar = crud_JyA.get_empleados_auxiliar()
    caballos = crud_JyA.get_caballos()
    
    if (not empleados_terapeuta_profesor) or (not empleados_conductor) or (not empleados_auxiliar) or (not caballos):
        flash('Debe asegurarse de que exista por lo menos un empleado terapeuta/profesor, conductor, auxiliar de pista y un caballo en el sistema', 'danger')
        return redirect("/JYA")
    else:
        return render_template("JYA/create_jya.html", empleados_terapeuta_profesor=empleados_terapeuta_profesor, empleados_conductor=empleados_conductor, empleados_auxiliar=empleados_auxiliar, caballos=caballos)

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
        "certificado_discapacidad": request.form["certificado_discapacidad"] == "true",
        "diagnostico_discapacidad": request.form.get("diagnostico_discapacidad", ""),
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
        "familiares_tutores": [
            {
                "parentesco": request.form["familiar1_parentesco"],
                "nombre": request.form["familiar1_nombre"],
                "apellido": request.form["familiar1_apellido"],
                "dni": request.form["familiar1_dni"],
                "domicilio_actual": request.form["familiar1_domicilio_actual"],
                "celular_actual": request.form["familiar1_celular_actual"],
                "email": request.form["familiar1_email"],
                "nivel_escolaridad": request.form["familiar1_nivel_escolaridad"],
                "ocupacion": request.form["familiar1_ocupacion"]
            },
            {
                "parentesco": request.form["familiar2_parentesco"],
                "nombre": request.form["familiar2_nombre"],
                "apellido": request.form["familiar2_apellido"],
                "dni": request.form["familiar2_dni"],
                "domicilio_actual": request.form["familiar2_domicilio_actual"],
                "celular_actual": request.form["familiar2_celular_actual"],
                "email": request.form["familiar2_email"],
                "nivel_escolaridad": request.form["familiar2_nivel_escolaridad"],
                "ocupacion": request.form["familiar2_ocupacion"]
            }
        ],
        "propuesta_trabajo": request.form["propuesta_trabajo"],
        "condicion_trabajo": request.form["condicion_trabajo"],
        "sede": request.form["sede"],
        "dias_asistencia": request.form.getlist("dias_asistencia"),
    }

    errores = validate_jya_form(jya_data)
    if errores:
        flash('Ocurrió un error al completar los campos, intentelo nuevamente...', 'danger')
        return redirect('/JYA/crear_jya')
    
    # Crear el JYA
    user = crud_JyA.create_jya(**jya_data)
    
    if not user:
        flash('El usuario ya existe o ocurrió un error', 'danger')
        return redirect('/JYA/crear_jya')
    
    # Asignar empleados (terapeuta, conductor, auxiliar) al JYA
    terapeuta_id = request.form["profesor_terapeuta_id"]
    conductor_id = request.form["conductor_caballo_id"]
    auxiliar_id = request.form["auxiliar_id"]

    crud_JyA.assign_employee_to_jya(user.id, terapeuta_id, 'terapeuta')
    crud_JyA.assign_employee_to_jya(user.id, conductor_id, 'conductor')
    crud_JyA.assign_employee_to_jya(user.id, auxiliar_id, 'auxiliar')

    flash('Usuario y empleados asignados correctamente', 'success')
    return redirect('/JYA')
    
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
        "certificado_discapacidad": request.form["certificado_discapacidad"] == "true",
        "diagnostico_discapacidad": request.form.get("diagnostico_discapacidad", ""),
        "tipo_discapacidad": request.form.get("tipo_discapacidad", None),
        "asignacion_familiar": request.form["asignacion_familiar"] == "true",
        "tipo_asignacion": request.form.get("tipo_asignacion", ""),
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
        "familiares_tutores": [
            {
                "parentesco": request.form["familiar1_parentesco"],
                "nombre": request.form["familiar1_nombre"],
                "apellido": request.form["familiar1_apellido"],
                "dni": request.form["familiar1_dni"],
                "domicilio_actual": request.form["familiar1_domicilio_actual"],
                "celular_actual": request.form["familiar1_celular_actual"],
                "email": request.form["familiar1_email"],
                "nivel_escolaridad": request.form["familiar1_nivel_escolaridad"],
                "ocupacion": request.form["familiar1_ocupacion"]
            },
            {
                "parentesco": request.form["familiar2_parentesco"],
                "nombre": request.form["familiar2_nombre"],
                "apellido": request.form["familiar2_apellido"],
                "dni": request.form["familiar2_dni"],
                "domicilio_actual": request.form["familiar2_domicilio_actual"],
                "celular_actual": request.form["familiar2_celular_actual"],
                "email": request.form["familiar2_email"],
                "nivel_escolaridad": request.form["familiar2_nivel_escolaridad"],
                "ocupacion": request.form["familiar2_ocupacion"]
            }
        ],
        "propuesta_trabajo": request.form["propuesta_trabajo"],
        "condicion_trabajo": request.form["condicion_trabajo"],
        "sede": request.form["sede"],
        "dias_asistencia": request.form.getlist("dias_asistencia"),
    }
    
    errores = validate_jya_form(jya_data)
    if errores:
        flash('Ocurrió un error al completar los campos, intentelo nuevamente...', 'danger')
        return redirect('/JYA/crear_jya')
    
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

@bp.get("/detalles/<int:jya_dni>")
@login_required
@check("jya_show")
def show_details_jya(jya_dni):
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    return render_template("JYA/show_jya.html", jya=jya)