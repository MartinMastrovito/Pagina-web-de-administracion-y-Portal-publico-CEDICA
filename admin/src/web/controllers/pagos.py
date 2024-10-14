from flask import Blueprint, render_template, request, redirect
from core.database import get_db
from src.core.models import Pagos
from sqlalchemy.orm import Session

pagos_bp = Blueprint("pagos", __name__, url_prefix="/pagos")

@pagos_bp.route('/', methods=['GET'])
def index():
    db= next(get_db())
    pagos = db.query(Pagos).all()
    return render_template('pagos/list_pagos.html', pagos=pagos)

@pagos_bp.route('/crear', methods=['GET'])
def crear_pago_form():
    return render_template('pagos/crear_pago.html')

@pagos_bp.route('/crear', methods=['POST'])
def crear_pago():
    db= next(get_db())
    nuevo_pago = {
        "beneficiario_id": request.form.get('beneficiario_id'),
        "monto": request.form['monto'],
        "tipo_pago": request.form['tipo_pago'],
        "descripcion": request.form.get('descripcion', "")
    }
    pago = Pagos(**nuevo_pago)
    db.add(pago)
    db.commit()
    return redirect('/pagos')

@pagos_bp.route('/actualizar/<int:pago_id>', methods=['GET'])
def actualizar_pago(pago_id):
    db= next(get_db())
    pago = db.query(Pagos).get(pago_id)
    return render_template('pagos/actualizar_pago.html', pago=pago)

@pagos_bp.route('/actualizar/<int:pago_id>', methods=['POST'])
def actualizar_pago(pago_id):
    db = next(get_db())
    pago = db.query(Pagos).get(pago_id)
    
    pago.monto = request.form['monto']####################DUDA:CON ACTUALIZAR BENEFICIARIO
    pago.tipo_pago = request.form['tipo_pago']
    pago.descripcion = request.form.get('descripcion', "")
    
    db.commit()
    return redirect('/pagos')

@pagos_bp.route('/eliminar/<int:pago_id>', methods=['POST'])
def delete_pago(pago_id):
    db= next(get_db())
    db.query(Pagos).filter(pago_id == pago_id).delete()
    db.commit()
    return redirect('/pagos')
