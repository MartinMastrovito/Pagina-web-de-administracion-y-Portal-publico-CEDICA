from flask import Blueprint, render_template, request, redirect
from core.database import db
from src.core.auth.models import Pago
from sqlalchemy.orm import Session
from datetime import datetime


pago_bp = Blueprint("pago", __name__, url_prefix="/pago", template_folder='../templates/pagos',static_folder="/admin/static")

@pago_bp.route('/listar', methods=['GET'])
def listar_pago():
    pago = db.query(Pago).all()
    return render_template('pagos/listar_pago.html')

@pago_bp.route('/crear', methods=['GET'])
def crear_pago_form():
    return render_template('pagos/crear_pago.html')

@pago_bp.route('/crear', methods=['POST'])
def crear_pago():
    nuevo_pago = {
        "beneficiario_id": request.form.get('beneficiario_id'),
        "monto": request.form['monto'],
        "tipo_pago": request.form['tipo_pago'],
        "descripcion": request.form.get('descripcion', "")
    }
    pago = Pago(**nuevo_pago)
    db.add(pago)
    db.commit()
    return redirect('/pago')

@pago_bp.route('/actualizar/<int:pago_id>', methods=['POST'])
def actualizar_pago(pago_id):
    pago = db.query(Pago).get(pago_id)
    
    pago.monto = request.form['monto']####################DUDA:CON ACTUALIZAR BENEFICIARIO
    pago.fecha = datetime.now()
    pago.tipo_pago = request.form['tipo_pago']
    pago.descripcion = request.form.get('descripcion', "")
    
    db.commit()
    return redirect('/pago')

@pago_bp.route('/eliminar/<int:pago_id>', methods=['POST'])
def eliminar_pago(pago_id):
    db.query(Pago).filter(pago_id == pago_id).delete()
    db.commit()
    return redirect('/pago')
