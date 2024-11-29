from src.core.database import db
from src.core.auth.models.model_pago import Pago
from src.core.auth.models.model_empleado import Empleados

def listar_pagos(payment_method=None, date_from=None, date_to=None, order='asc', page=1, per_page=10):
    """
    Lista los pagos de forma paginada.

    Args:
        payment_method: Forma de pago del pago.
        date_from: Fecha inicial para filtrar pagos.
        date_to: Fecha final para filtrar pagos.
        order: Orden de la lista ('asc' o 'desc').
        page: El número de la página a obtener. Por defecto es 1.
        per_page: El número de elementos por página. Por defecto es 10.

    Returns:
        Pagination: Un objeto de paginación que contiene los pagos.
    """
    
    query = Pago.query
    
    if payment_method:
        query = query.filter_by(tipo_pago=payment_method)

    if date_from:
        query = query.filter(Pago.fecha_pago >= date_from)
    if date_to:
        query = query.filter(Pago.fecha_pago <= date_to)

    if order == 'asc':
        query = query.order_by(Pago.fecha_pago.asc())
    else:
        query = query.order_by(Pago.fecha_pago.desc())

    return query.paginate(page=page, per_page=per_page, error_out=False)

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
    
def get_empleado(empleado_id):
    return Empleados.query.get(empleado_id)