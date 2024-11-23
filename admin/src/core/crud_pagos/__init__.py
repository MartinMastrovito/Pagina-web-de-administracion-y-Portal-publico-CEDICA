"""
Módulo de operaciones CRUD para la gestión de pagos.

Este módulo contiene las funciones para listar, obtener, crear, actualizar y eliminar pagos en la base de datos.
"""

from src.core.database import db
from src.core.auth.models.model_pago import Pago

def listar_pagos(page=1, per_page=10):
    """
    Lista los pagos de forma paginada.

    Args:
        page (int): El número de la página a obtener. Por defecto es 1.
        per_page (int): El número de elementos por página. Por defecto es 10.

    Returns:
        Pagination: Un objeto de paginación que contiene los pagos.
    """
    return Pago.query.paginate(page=page, per_page=per_page, error_out=False)

def obtener_pago(id):
    """
    Obtiene un pago por su ID.

    Args:
        id (int): El ID del pago a obtener.

    Returns:
        Pago: El objeto Pago correspondiente al ID proporcionado.
    """
    return Pago.query.get_or_404(id)

def crear_pago(data):
    """
    Crea un nuevo pago en la base de datos.

    Args:
        data (dict): Un diccionario con los datos del nuevo pago.

    Returns:
        Pago: El objeto Pago creado.
    """
    nuevo_pago = Pago(**data)
    db.session.add(nuevo_pago)
    db.session.commit()
    return nuevo_pago

def actualizar_pago(id, data):
    """
    Actualiza un pago existente en la base de datos.

    Args:
        id (int): El ID del pago a actualizar.
        data (dict): Un diccionario con los datos actualizados del pago.

    Returns:
        Pago: El objeto Pago actualizado.
    """
    pago = Pago.query.get_or_404(id)
    for key, value in data.items():
        setattr(pago, key, value)
    db.session.commit()
    return pago

def eliminar_pago(id):
    """
    Elimina un pago de la base de datos.

    Args:
        id (int): El ID del pago a eliminar.

    Returns:
        None
    """
    pago = Pago.query.get_or_404(id)
    db.session.delete(pago)
    db.session.commit()