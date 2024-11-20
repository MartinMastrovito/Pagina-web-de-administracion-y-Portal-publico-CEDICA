from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.crud_caballos import (
    search_caballos, create_caballo, get_caballo_by_id,
    update_caballo, delete_caballo, list_documents
)
from src.core.auth.models.model_documento import Documento
from src.core.auth.decorators import login_required, check
from src.core.auth.models.model_miembroEquipo import MiembroEquipo

# Definir el blueprint para caballos
caballos_bp = Blueprint('caballos', __name__, url_prefix='/caballos')

@caballos_bp.route('/', methods=['GET'])
@login_required
@check("horse_index")
def menu_caballos():
    """
    Muestra el menú principal de caballos con paginación y filtros.

    Returns:
        str: Renderiza la plantilla 'caballos/index.html' con los caballos paginados y los filtros aplicados.
    """
    page = request.args.get('page', 1, type=int)
    nombre = request.args.get('nombre', '', type=str)
    tipo_ja_asignado = request.args.get('tipo_ja_asignado', '', type=str)  
    orden = request.args.get('orden', 'nombre')
    direction = request.args.get('direction', 'asc')

    caballos_paginados = search_caballos(nombre=nombre, tipo_ja_asignado=tipo_ja_asignado, sort_by=orden, order=direction, page=page)

    return render_template('caballos/index.html', caballos=caballos_paginados, nombre=nombre, tipo_ja_asignado=tipo_ja_asignado, orden=orden, direction=direction)

@caballos_bp.route('/<int:id>', methods=['GET'])
@login_required
@check("horse_show")
def mostrar_caballo(id):
    """
    Muestra los detalles de un caballo específico.

    Args:
        id (int): ID del caballo a mostrar.

    Returns:
        str: Renderiza la plantilla 'caballos/show.html' con los detalles del caballo y sus documentos.
    """
    caballo = get_caballo_by_id(id)
    documentos = list_documents(caballo_id=caballo.id)
    return render_template('caballos/show.html', caballo=caballo, documentos=documentos)

@caballos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@check("horse_new")
def crear_caballo():
    """
    Crea un nuevo caballo. Muestra el formulario de creación y procesa los datos enviados.

    Returns:
        str: Renderiza la plantilla 'caballos/nuevo.html' con el formulario de creación.
        Redirect: Redirige al menú de caballos después de crear un nuevo caballo.
    """
    opciones_ja = ["Hipoterapia", "Monta_Terapéutica", "Deporte_Ecuestre_Adaptado", "Actividades_Recreativas", "Equitación"]
    
    if request.method == 'POST':
        datos_caballo = {
            'nombre': request.form['nombre'],
            'fecha_nacimiento': request.form['fecha_nacimiento'],
            'sexo': request.form['sexo'],
            'raza': request.form['raza'],
            'pelaje': request.form['pelaje'],
            'tipo_ingreso': request.form['tipo_ingreso'],
            'fecha_ingreso': request.form['fecha_ingreso'],
            'sede_asignada': request.form['sede_asignada'],
            'tipo_ja_asignado': request.form.getlist('tipo_ja_asignado')  # Recoge la selección
        }
        datos_caballo['tipo_ja_asignado'] = ', '.join(datos_caballo['tipo_ja_asignado'])  # Convierte la lista a string
        nuevo_caballo = create_caballo(**datos_caballo)
        flash('Caballo creado exitosamente.', 'success')
        return redirect(url_for('caballos.menu_caballos'))
    
    return render_template('caballos/nuevo.html', opciones_ja=opciones_ja)

@caballos_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@check("horse_delete")
def eliminar_caballo(id):
    """
    Elimina un caballo específico.

    Args:
        id (int): ID del caballo a eliminar.

    Returns:
        Redirect: Redirige al menú de caballos después de eliminar el caballo.
    """
    delete_caballo(id)
    flash('Caballo eliminado exitosamente.', 'success')
    return redirect(url_for('caballos.menu_caballos'))

@caballos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@check("horse_update")
def editar_caballo(id):
    """
    Edita un caballo específico. Muestra el formulario de edición y procesa los datos enviados.

    Args:
        id (int): ID del caballo a editar.

    Returns:
        str: Renderiza la plantilla 'caballos/editar.html' con el formulario de edición.
        Redirect: Redirige al menú de caballos después de editar el caballo.
    """
    caballo = get_caballo_by_id(id)
    if request.method == 'POST':
        datos_actualizados = {
            'nombre': request.form['nombre'],
            'fecha_nacimiento': request.form['fecha_nacimiento'],
            'sexo': request.form['sexo'],
            'raza': request.form['raza'],
            'pelaje': request.form['pelaje'],
            'tipo_ingreso': request.form['tipo_ingreso'],
            'fecha_ingreso': request.form['fecha_ingreso'],
            'sede_asignada': request.form['sede_asignada'],
        }
        update_caballo(id, **datos_actualizados)
        flash('Caballo editado exitosamente.', 'success')
        return redirect(url_for('caballos.menu_caballos'))
    return render_template('caballos/editar.html', caballo=caballo)