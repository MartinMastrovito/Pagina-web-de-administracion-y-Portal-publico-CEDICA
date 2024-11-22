from src.core.database import db
from src.core.auth.models.model_pago import Pago

def listar_pagos():
    return Pago.query.all()

def obtener_pago(id):
    return Pago.query.get_or_404(id)

def crear_pago(data):
    nuevo_pago = Pago(**data)
    db.session.add(nuevo_pago)
    db.session.commit()
    return nuevo_pago

def actualizar_pago(id, data):
    pago = Pago.query.get_or_404(id)
    for key, value in data.items():
        setattr(pago, key, value)
    db.session.commit()
    return pago

def eliminar_pago(id):
    pago = Pago.query.get_or_404(id)
    db.session.delete(pago)
    db.session.commit()