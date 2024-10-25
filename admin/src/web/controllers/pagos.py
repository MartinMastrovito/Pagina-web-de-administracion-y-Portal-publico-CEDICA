from flask import Blueprint, render_template, request, redirect, flash, url_for
from core.database import db
from src.core.auth.models.model_pago import Pago
from datetime import datetime
from src.core.auth.models.model_empleado import Empleados
from sqlalchemy import asc, desc


pago_bp = Blueprint('pago', __name__, url_prefix="/pago", template_folder='../templates/pagos',static_folder="/admin/static")

@pago_bp.route('/listar_pago', methods=['GET'])
def listar_pago():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    tipo_pago = request.args.get('tipo_pago')
    orden = request.args.get('orden', 'asc')
    query = Pago.query
    if fecha_inicio and fecha_fin:
        query = query.filter(Pago.fecha_pago.between(fecha_inicio, fecha_fin))
    if tipo_pago:
        query = query.filter(Pago.tipo_pago == tipo_pago)
    if orden == 'asc':
        query = query.order_by(asc(Pago.fecha_pago))
    else:
        query = query.order_by(desc(Pago.fecha_pago))
    pagos = query.all()
    return render_template('pagos/listar_pago.html', pagos=pagos)

@pago_bp.route('/crear_pago', methods=['GET'])
def crear_pago_form():
    empleados = Empleados.query.all()
    return render_template('pagos/crear_pago.html', empleados = empleados)

@pago_bp.post('/crear_pago')
#@login_required
def crear_pago():
    nuevo_pago = {
        "beneficiario_id": request.form.get('id'),
        "monto": request.form['monto'],
        "fecha_pago": request.form['fecha_pago'],
        "tipo_pago": request.form['tipo_pago'],
        "description": request.form.get('description', "")
    }
    pago = Pago(**nuevo_pago)
    try:
        db.session.add(pago)
        db.session.commit()
        flash('Empleado creado exitosamente', 'success')

        return redirect(url_for('pago.crear_pago_form'))
    except Exception as e:
        db.session.rollback()
        flash('Ocurrió un error al crear un pago: ' + str(e), 'danger')
        return redirect(url_for('pago.crear_pago_form'))

@pago_bp.route('/actualizar/<int:pago_id>', methods=['POST'])
def actualizar_pago(pago_id):
    pago = Pago.query.get(pago_id)
    
    pago.monto = request.form['monto']
    pago.fecha = request.form['fecha_pago']
    pago.tipo_pago = request.form['tipo_pago']
    pago.descripcion = request.form.get('descripcion', "")
    
    db.session.commit()
    return redirect(url_for('pago.crear_pago_form'))

@pago_bp.route('/eliminar/<int:pago_id>', methods=['POST'])
def eliminar_pago(pago_id):
    Pago.query.filter_by(id=pago_id).delete()
    db.session.commit()
    return redirect(url_for('pago.crear_pago_form'))
