from src.core.database import db
from src.core.auth.models.model_consulta import Consulta
from sqlalchemy import asc, desc

def search_consultas(nombre_completo=None, estado=None, sort_by='fecha', order='asc', page=1, per_page=10):
    """
    Busca consultas con filtros opcionales y paginación.

    Args:
        nombre_completo (str, optional): Nombre completo para filtrar las consultas.
        estado (str, optional): Estado para filtrar las consultas.
        sort_by (str, optional): Columna por la cual ordenar las consultas. Por defecto es 'fecha'.
        order (str, optional): Orden de la columna ('asc' para ascendente, 'desc' para descendente). Por defecto es 'asc'.
        page (int, optional): Número de página para la paginación. Por defecto es 1.
        per_page (int, optional): Número de elementos por página. Por defecto es 10.

    Returns:
        Pagination: Objeto de paginación con las consultas filtradas y ordenadas.
    """
    query = Consulta.query

    if nombre_completo:
        query = query.filter(Consulta.nombre_completo.ilike(f"%{nombre_completo}%"))
    
    if estado:
        query = query.filter(Consulta.estado.ilike(f"%{estado}%"))

    sort_column = Consulta.fecha
    
    query = query.order_by(asc(sort_column) if order == 'asc' else desc(sort_column))

    return query.paginate(page=page, per_page=per_page, error_out=False)

def create_consulta(**kwargs):
    """
    Crea una nueva consulta.

    Args:
        **kwargs: Atributos de la consulta a crear.

    Returns:
        Consulta: La consulta creada.
    """
    consulta = Consulta(**kwargs)
    db.session.add(consulta)
    db.session.commit()
    return consulta

def get_consulta_by_id(id):
    """
    Obtiene una consulta por su ID.

    Args:
        id (int): ID de la consulta a obtener.

    Returns:
        Consulta: La consulta obtenida.
    """
    return Consulta.query.get_or_404(id)

def update_consulta(id, **kwargs):
    """
    Actualiza una consulta existente.

    Args:
        id (int): ID de la consulta a actualizar.
        **kwargs: Atributos de la consulta a actualizar.

    Returns:
        Consulta: La consulta actualizada.
    """
    consulta = get_consulta_by_id(id)
    for key, value in kwargs.items():
        setattr(consulta, key, value)
    db.session.commit()
    return consulta

def delete_consulta(id):
    """
    Elimina una consulta por su ID.

    Args:
        id (int): ID de la consulta a eliminar.
    """
    consulta = get_consulta_by_id(id)
    db.session.delete(consulta)
    db.session.commit()