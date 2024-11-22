from flask import Blueprint, render_template, request, redirect, flash
from src.core.crud_pagos import obtener_pagos, crear_pago, actualizar_pago, eliminar_pago
from src.core.invoices.utiles import get_all_employees

pago_bp = Blueprint("pago", __name__, url_prefix="/pago", template_folder='../templates/pagos', static_folder="/admin/static")

@pago_bp.route('/listar', methods=['GET'])
def listar_pago():
    filtros = {
        'fecha_inicio': request.args.get('fecha_inicio'),
        'fecha_fin': request.args.get('fecha_fin'),
        'tipo_pago': request.args.get('tipo_pago'),
        'orden': request.args.get('orden', 'asc')
    }
    pagos = obtener_pagos(filtros)
    return render_template('pagos/listar_pago.html', pagos=pagos)

@pago_bp.route('/crear', methods=['GET', 'POST'])
def crear_pago_route():
    if request.method == 'POST':
        datos = {
            "beneficiario_id": request.form.get('beneficiario_id'),
            "monto": request.form['monto'],
            "fecha_pago": request.form['fecha_pago'],
            "tipo_pago": request.form['tipo_pago'],
            "descripcion": request.form.get('descripcion', "")
        }
        crear_pago(datos)
        flash("Pago creado exitosamente", 'success')
        return redirect('/pago/listar')
    empleados = get_all_employees()
    return render_template('pagos/crear_pago.html', empleados=empleados)

@pago_bp.route('/actualizar/<int:pago_id>', methods=['POST'])
def actualizar_pago_route(pago_id):
    datos = {
        "monto": request.form['monto'],
        "tipo_pago": request.form['tipo_pago'],
        "descripcion": request.form.get('descripcion', "")
    }
    actualizar_pago(pago_id, datos)
    flash("Pago actualizado correctamente", 'success')
    return redirect('/pago/listar')

@pago_bp.route('/eliminar', methods=['POST'])
def eliminar_pago_route():
    pago_id = request.form['id']
    eliminar_pago(pago_id)
    flash("Pago eliminado correctamente", 'success')
    return redirect('/pago/listar')
