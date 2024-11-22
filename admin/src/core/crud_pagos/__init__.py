from src.core.database import db
from src.core.auth.models.model_pago import Pago
from datetime import datetime

def obtener_pagos(filtros):
    query = Pago.query
    if filtros.get('fecha_inicio') and filtros.get('fecha_fin'):
        query = query.filter(Pago.fecha_pago.between(filtros['fecha_inicio'], filtros['fecha_fin']))
    if filtros.get('tipo_pago'):
        query = query.filter(Pago.tipo_pago == filtros['tipo_pago'])
    orden = filtros.get('orden', 'asc')
    query = query.order_by(Pago.fecha_pago.asc() if orden == 'asc' else Pago.fecha_pago.desc())
    return query.all()

def crear_pago(datos):
    pago = Pago(**datos)
    db.session.add(pago)
    db.session.commit()
    return pago

def actualizar_pago(pago_id, datos):
    pago = Pago.query.get_or_404(pago_id)
    for key, value in datos.items():
        setattr(pago, key, value)
    db.session.commit()
    return pago

def eliminar_pago(pago_id):
    Pago.query.filter_by(id=pago_id).delete()
    db.session.commit()
