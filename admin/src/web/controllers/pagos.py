from flask import Blueprint, render_template, request, redirect, flash
from src.core.database import db
from src.core.auth.models.model_pago import Pago
from src.core.auth.models.model_empleado import Empleados
from src.core.invoices import utiles
from datetime import datetime
from sqlalchemy import asc, desc


pago_bp = Blueprint("pago", __name__, url_prefix="/pago", template_folder='../templates/pagos',static_folder="/admin/static")

@pago_bp.route('/listar', methods=['GET'])
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
        query = query.order_by(Pago.fecha_pago.asc())
    else:
        query = query.order_by(Pago.fecha_pago.desc())
    pagos = query.all()
    return render_template('pagos/listar_pago.html',pagos=pagos)

@pago_bp.route('/crear', methods=['GET'])
def crear_pago_form():
    employees = utiles.get_all_employees()
    return render_template('pagos/crear_pago.html',pago=pago_bp,empleados = employees)

@pago_bp.route('/crear', methods=['POST'])
def crear_pago():
    nuevo_pago = {
        "beneficiario_id": request.form.get('beneficiario_id'),
        "monto": request.form['monto'],
        "fecha_pago": request.form['fecha_pago'],
        "tipo_pago": request.form['tipo_pago'],
        "descripcion": request.form.get('descripcion', "")
    }
    empleado = Empleados.query.get_or_404(nuevo_pago['beneficiario_id'])
    nuevo_pago['beneficiario_nombre'] = empleado.nombre
    nuevo_pago['beneficiario_apellido'] = empleado.apellido
    pago = Pago(**nuevo_pago)
    db.session.add(pago)
    db.session.commit()
    flash("Se creo el pago",'true')
    return redirect('/pago/crear')

@pago_bp.route('/actualizar/<int:pago_id>', methods=['POST'])
def actualizar_pago(pago_id):
    pago = db.query(Pago).get(pago_id)
    
    pago.monto = request.form['monto']
    pago.fecha = datetime.now()
    pago.tipo_pago = request.form['tipo_pago']
    pago.descripcion = request.form.get('descripcion', "")
    db.commit()
    return redirect('/pago')

@pago_bp.route('/eliminar/', methods=['POST'])
def eliminar_pago():
    pago_id = request.form['id']
    db.session.query(Pago).filter_by(id = pago_id).delete()
    db.session.commit()
    return redirect('/pago/listar')
