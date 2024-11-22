from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from src.core.crud_pagos import listar_pagos, obtener_pago, crear_pago, actualizar_pago, eliminar_pago
from src.core.auth.models.model_empleado import Empleados
from src.core.database import db
from src.core.empleados import listar_empleados_activos  # Importar la función de empleados

pagos_bp = Blueprint('pagos', __name__, url_prefix='/pagos')

@pagos_bp.route('/', methods=['GET'])
def listar_pagos_route():
    page = request.args.get('page', 1, type=int)
    pagos = listar_pagos(page=page)
    return render_template('pagos/listar_pago.html', pagos=pagos)

@pagos_bp.route('/<int:id>', methods=['GET'])
def obtener_pago_route(id):
    pago = obtener_pago(id)
    return render_template('pagos/mostrar_pago.html', pago=pago)

@pagos_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_pago_route():
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
def actualizar_pago_route(id):
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
def eliminar_pago_route():
    pago_id = request.form['id']
    eliminar_pago(pago_id)
    flash("Pago eliminado correctamente", 'success')
    return redirect(url_for('pagos.listar_pagos_route'))