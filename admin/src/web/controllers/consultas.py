from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.core import crud_consultas as crud_consulta
from src.core.auth.decorators import login_required, check
from datetime import datetime

consultas_bp = Blueprint('consultas', __name__, url_prefix='/consultas')

@consultas_bp.route('/', methods=['GET'])
@login_required
@check("consulta_index")
def menu_consultas():
    """
    Muestra el menú de consultas con opciones de búsqueda, ordenamiento y filtrado.

    Returns:
        Renderizado de la plantilla index.html con las consultas paginadas.
    """
    page = request.args.get('page', 1, type=int)
    nombre_completo = request.args.get('nombre_completo', '', type=str)
    estado = request.args.get('estado', '', type=str)
    orden = request.args.get('orden', 'fecha')
    direction = request.args.get('direction', 'asc')
    
    consultas_paginadas = crud_consulta.search_consultas(
        nombre_completo=nombre_completo,
        estado=estado,
        sort_by=orden,
        order=direction,
        page=page,
    )

    return render_template('consultas/index_consultas.html', consultas=consultas_paginadas.items, pagination=consultas_paginadas, nombre_completo=nombre_completo, estado=estado, orden=orden, direction=direction)

@consultas_bp.route('/<int:id>', methods=['GET'])
@login_required
@check("consulta_show")
def mostrar_consulta(id):
    """
    Muestra los detalles de una consulta específica.

    Args:
        id (int): ID de la consulta a mostrar.

    Returns:
        Renderizado de la plantilla show.html con los detalles de la consulta.
    """
    consulta = crud_consulta.get_consulta_by_id(id)
    return render_template('consultas/show_consultas.html', consulta=consulta)

@consultas_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@check("consulta_new")
def nueva_consulta():
    """
    Crea una nueva consulta.

    Returns:
        Renderizado de la plantilla nuevo.html para GET.
        Redirección al menú de consultas para POST.
    """
    if request.method == 'POST':
        datos_consulta = {
            'nombre_completo': request.form['nombre_completo'],
            'email': request.form['email'],
            'fecha': request.form['fecha'],
            'descripcion': request.form['descripcion'],
            'estado': request.form['estado']
        }
        nueva_consulta = crud_consulta.create_consulta(**datos_consulta)
        flash('Consulta creada exitosamente.', 'success')
        return redirect(url_for('consultas.menu_consultas'))
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('consultas/new_consultas.html', current_date=current_date)

@consultas_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@check("consulta_update")
def editar_consulta(id):
    """
    Edita una consulta existente.

    Args:
        id (int): ID de la consulta a editar.

    Returns:
        Renderizado de la plantilla editar.html para GET.
        Redirección al menú de consultas para POST.
    """
    consulta = crud_consulta.get_consulta_by_id(id)
    
    if request.method == 'POST':
        datos_consulta = {
            'estado': request.form['estado'],
            'cambio_estado': request.form.get('cambio_estado', '')
        }
        crud_consulta.update_consulta(id, **datos_consulta)
        flash('Consulta actualizada exitosamente.', 'success')
        return redirect(url_for('consultas.menu_consultas'))
    
    return render_template('consultas/editar_consultas.html', consulta=consulta)

@consultas_bp.post('/<int:id>/eliminar')
@login_required
@check("consulta_destroy")
def eliminar_consulta(id):
    """
    Elimina una consulta existente.

    Args:
        id (int): ID de la consulta a eliminar.

    Returns:
        Redirección al menú de consultas.
    """
    crud_consulta.delete_consulta(id)
    flash('Consulta eliminada exitosamente.', 'success')
    return redirect(url_for('consultas.menu_consultas'))



