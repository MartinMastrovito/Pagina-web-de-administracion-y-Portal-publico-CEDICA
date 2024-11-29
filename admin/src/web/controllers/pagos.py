"""
Módulo de controladores para la gestión de pagos.

Este módulo contiene las rutas y controladores para listar, obtener, crear, actualizar y eliminar pagos.
"""

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from src.core.auth.decorators import check, login_required
from src.core.crud_pagos import listar_pagos, obtener_pago, crear_pago, actualizar_pago, eliminar_pago
from src.core.auth.models.model_empleado import Empleados
from src.core.database import db
from src.core.empleados import listar_empleados_activos

pagos_bp = Blueprint('pagos', __name__, url_prefix='/pagos')

@pagos_bp.route('/', methods=['GET'])
@login_required
@check("payment_index")
def listar_pagos_route():
    """
    Ruta para listar los pagos.

    Obtiene una lista paginada de pagos y la renderiza en el template 'listar_pago.html'.

    Returns:
        str: El contenido HTML de la página de listado de pagos.
    """
    page = request.args.get('page', 1, type=int)
    pagos = listar_pagos(page=page)
    return render_template('pagos/listar_pago.html', pagos=pagos)

@pagos_bp.route('/<int:id>', methods=['GET'])
@login_required
@check("payment_show")
def obtener_pago_route(id):
    """
    Ruta para obtener los detalles de un pago específico.

    Obtiene los detalles de un pago por su ID y los renderiza en el template 'mostrar_pago.html'.

    Args:
        id (int): El ID del pago a obtener.

    Returns:
        str: El contenido HTML de la página de detalles del pago.
    """
    pago = obtener_pago(id)
    return render_template('pagos/mostrar_pago.html', pago=pago)

@pagos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@check("payment_new")
def crear_pago_route():
    """
    Ruta para crear un nuevo pago.

    Muestra el formulario para crear un nuevo pago y maneja la lógica para guardar el pago en la base de datos.

    Returns:
        str: El contenido HTML de la página de creación de pago o una redirección a la lista de pagos.
    """
    if request.method == 'POST':
        data = request.form.to_dict()
        empleado_id = data.get('beneficiario_id')
        empleado = Empleados.query.get(empleado_id)
        if empleado:
            data['beneficiario_nombre'] = empleado.nombre
            data['beneficiario_apellido'] = empleado.apellido
            data['beneficiario_id'] = empleado.id
        nuevo_pago = crear_pago(data)
        flash("Pago creado correctamente", 'success')
        return redirect(url_for('pagos.listar_pagos_route'))

    empleados = listar_empleados_activos()  # Obtener empleados activos
    return render_template('pagos/crear_pago.html', empleados=empleados)

@pagos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@check("payment_update")
def actualizar_pago_route(id):
    """
    Ruta para actualizar un pago existente.

    Muestra el formulario para editar un pago y maneja la lógica para actualizar el pago en la base de datos.

    Args:
        id (int): El ID del pago a actualizar.

    Returns:
        str: El contenido HTML de la página de edición de pago o una redirección a la lista de pagos.
    """
    pago = obtener_pago(id)
    if request.method == 'POST':
        data = request.form.to_dict()
        empleado_id = data.get('beneficiario_id')
        empleado = Empleados.query.get(empleado_id)
        if empleado:
            data['beneficiario_nombre'] = empleado.nombre
            data['beneficiario_apellido'] = empleado.apellido
            data['beneficiario_id'] = empleado.id
        actualizar_pago(id, data)
        flash("Pago actualizado correctamente", 'success')
        return redirect(url_for('pagos.listar_pagos_route'))
    empleados = listar_empleados_activos()  # Obtener empleados activos
    return render_template('pagos/editar_pago.html', pago=pago, empleados=empleados)

@pagos_bp.route('/eliminar', methods=['POST'])
@login_required
@check("payment_destroy")
def eliminar_pago_route():
    """
    Ruta para eliminar un pago.

    Maneja la lógica para eliminar un pago de la base de datos.

    Returns:
        str: Una redirección a la lista de pagos.
    """
    pago_id = request.form['id']
    eliminar_pago(pago_id)
    flash("Pago eliminado correctamente", 'success')
    return redirect(url_for('pagos.listar_pagos_route'))