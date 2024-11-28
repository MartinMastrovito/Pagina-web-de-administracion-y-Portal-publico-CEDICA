from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.crud_caballos import (
    search_caballos, create_caballo, get_caballo_by_id,
    update_caballo, delete_caballo, list_documents, get_empleados_by_rol , get_empleados_by_ids
)
from src.core.auth.decorators import login_required, check


caballos_bp = Blueprint('caballos', __name__, url_prefix='/caballos')

@caballos_bp.route('/', methods=['GET'])
@login_required
@check("horse_index")
def menu_caballos():
    """
    Muestra el menú principal de caballos con paginación y filtros.
    """
    page = request.args.get('page', 1, type=int)
    nombre = request.args.get('nombre', '', type=str)
    tipo_ja_asignado = request.args.get('tipo_ja_asignado', '', type=str)  
    orden = request.args.get('orden', 'nombre')
    direction = request.args.get('direction', 'asc')

    caballos_paginados = search_caballos(nombre=nombre, tipo_ja_asignado=tipo_ja_asignado, sort_by=orden, order=direction, page=page)

    return render_template('caballos/index.html', caballos=caballos_paginados, nombre=nombre, tipo_ja_asignado=tipo_ja_asignado, orden=orden, direction=direction)


@caballos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@check("horse_new")
def crear_caballo():
    """
    Crea un nuevo caballo. Muestra el formulario de creación y procesa los datos enviados.
    """
    opciones_ja = ["Hipoterapia", "Monta_Terapéutica", "Deporte_Ecuestre_Adaptado", "Actividades_Recreativas", "Equitación"]

    if request.method == 'POST':
        try:
            datos_caballo = {
                'nombre': request.form['nombre'],
                'fecha_nacimiento': request.form['fecha_nacimiento'],
                'sexo': request.form['sexo'],
                'raza': request.form['raza'],
                'pelaje': request.form['pelaje'],
                'tipo_ingreso': request.form['tipo_ingreso'],
                'fecha_ingreso': request.form['fecha_ingreso'],
                'sede_asignada': request.form['sede_asignada'],
                'tipo_ja_asignado': request.form.getlist('tipo_ja_asignado')
            }
            datos_caballo['tipo_ja_asignado'] = ', '.join(datos_caballo['tipo_ja_asignado'])

            entrenadores_ids = request.form.getlist('entrenadores_ids', type=int) or []
            conductores_ids = request.form.getlist('conductores_ids', type=int) or []

            create_caballo(
                **datos_caballo,
                entrenadores_ids=entrenadores_ids,
                conductores_ids=conductores_ids
            )

            flash('Caballo registrado correctamente', 'success')
            return redirect(url_for('caballos.menu_caballos'))
        except Exception as e:
            flash(f'Error al registrar el caballo: {e}', 'danger')

    entrenadores = get_empleados_by_rol('Entrenador de Caballos')
    conductores = get_empleados_by_rol('Conductor')
    return render_template(
        'caballos/nuevo.html', 
        opciones_ja=opciones_ja,
        entrenadores=entrenadores,
        conductores=conductores
    )


@caballos_bp.route('/<int:id>', methods=['GET'])
@login_required
@check("horse_show")
def mostrar_caballo(id):
    """
    Muestra los detalles de un caballo, incluyendo entrenadores y coordinadores asignados.
    """
    caballo = get_caballo_by_id(id)
    
    entrenadores_ids = [entrenador.id for entrenador in caballo.entrenadores]
    conductores_ids = [conductor.id for conductor in caballo.conductores]

    entrenadores = get_empleados_by_ids(entrenadores_ids)
    conductores = get_empleados_by_ids(conductores_ids)

    return render_template('caballos/show.html', caballo=caballo, entrenadores=entrenadores, conductores=conductores)

@caballos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@check("horse_update")
def editar_caballo(id):
    """
    Permite editar un caballo existente, mostrando entrenadores y conductores asignados.
    """
    caballo = get_caballo_by_id(id)

    if request.method == 'POST':
        try:
            datos_caballo = {
                'nombre': request.form['nombre'],
                'fecha_nacimiento': request.form['fecha_nacimiento'],
                'sexo': request.form['sexo'],
                'raza': request.form['raza'],
                'pelaje': request.form['pelaje'],
                'tipo_ingreso': request.form['tipo_ingreso'],
                'fecha_ingreso': request.form['fecha_ingreso'],
                'sede_asignada': request.form['sede_asignada'],
                'tipo_ja_asignado': ', '.join(request.form.getlist('tipo_ja_asignado'))
            }

            entrenadores_ids = request.form.getlist('entrenadores', type=int)
            conductores_ids = request.form.getlist('conductores', type=int)

            update_caballo(
                id,
                **datos_caballo,
                entrenadores_ids=entrenadores_ids,
                conductores_ids=conductores_ids
            )

            flash('Caballo actualizado correctamente', 'success')
            return redirect(url_for('caballos.menu_caballos'))
        except Exception as e:
            flash(f'Error al actualizar el caballo: {e}', 'danger')

    entrenadores = get_empleados_by_rol('Entrenador de Caballos')
    conductores = get_empleados_by_rol('Conductor')

    return render_template(
        'caballos/editar.html', 
        caballo=caballo, 
        entrenadores=entrenadores, 
        conductores=conductores
    )



@caballos_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@check("horse_destroy")
def eliminar_caballo(id):
    """
    Elimina un caballo de la base de datos.
    """
    try:
        delete_caballo(id)
        flash('Caballo eliminado correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar el caballo: {e}', 'danger')
    return redirect(url_for('caballos.menu_caballos'))