from flask import Blueprint, render_template, request, redirect
from core.database import db
from core.auth.models.model_pago import Pago
from datetime import datetime


pago_bp = Blueprint("pago", __name__, url_prefix="/pago", template_folder='../templates/pagos',static_folder="/admin/static")

@pago_bp.route('/listar', methods=['GET'])
def listar_pago():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    tipo_pago = request.args.get('tipo_pago')
    orden = request.args.get('orden', 'asc')
    query = db.session.query(Pago)
    if fecha_inicio and fecha_fin:
        query = query.filter(Pago.fecha_pago.between(fecha_inicio, fecha_fin))
    if tipo_pago:
        query = query.filter(Pago.tipo_pago == tipo_pago)
    if orden == 'asc':
        query = query.order_by(Pago.fecha_pago.asc())
    else:
        query = query.order_by(Pago.fecha_pago.desc())
    pagos = query.all()
    return render_template('pagos/listar_pago.html', pagos=pagos)

@pago_bp.route('/crear', methods=['GET'])
def crear_pago_form():
    empleados = db.session.query(Pago.beneficiario_id).all()
    return render_template('pagos/crear_pago.html', empleados = empleados)

@pago_bp.route('/crear', methods=['GET', 'POST'])
#@login_required
def crear_pago():
    if request.method == 'POST':
        nuevo_pago = {
            "beneficiario_id": request.form.get('id'),
            "monto": request.form['monto'],
            "fecha_pago": request.form['fecha_pago'],
            "tipo_pago": request.form['tipo_pago'],
            "descripcion": request.form.get('descripcion', "")
        }
        pago = Pago(**nuevo_pago)
        db.add(pago)
        db.commit()
    return redirect('/pagos/crear_pago.html')

@pago_bp.route('/actualizar/<int:pago_id>', methods=['POST'])
def actualizar_pago(pago_id):
    pago = Pago.query.get(pago_id)
    
    pago.monto = request.form['monto']
    pago.fecha = datetime.now()
    pago.tipo_pago = request.form['tipo_pago']
    pago.descripcion = request.form.get('descripcion', "")
    
    db.session.commit()
    return redirect('/pagos/crear_pago.html')

@pago_bp.route('/eliminar/<int:pago_id>', methods=['POST'])
def eliminar_pago(pago_id):
    db.query(Pago).filter(Pago.id == pago_id).delete()
    db.session.commit()
    return redirect('/pagos/crear_pago.html')
