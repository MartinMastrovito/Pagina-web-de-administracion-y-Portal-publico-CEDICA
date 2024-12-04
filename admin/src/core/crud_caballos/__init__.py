from src.core.database import db
from src.core.auth.models.model_caballos import Caballo
from src.core.auth.models.model_documento import Documento
from sqlalchemy import asc, desc
from werkzeug.utils import secure_filename
from minio import Minio
from minio.error import S3Error
from src.core.auth.models.model_empleado import Empleados as Empleado
from flask import abort
def search_caballos(nombre=None, tipo_ja_asignado=None, sort_by='nombre', order='asc', page=1, per_page=10):
    """
    Busca caballos con filtros opcionales y paginación.

    Args:
        nombre (str, optional): Nombre del caballo para filtrar.
        tipo_ja_asignado (str, optional): Tipo de actividad asignada para filtrar.
        sort_by (str, optional): Columna por la cual ordenar los resultados. Por defecto es 'nombre'.
        order (str, optional): Orden de la columna ('asc' para ascendente, 'desc' para descendente). Por defecto es 'asc'.
        page (int, optional): Número de página para la paginación. Por defecto es 1.
        per_page (int, optional): Número de elementos por página. Por defecto es 10.

    Returns:
        Pagination: Objeto de paginación con los caballos filtrados y ordenados.
    """
    query = db.session.query(Caballo)
    query = query.filter(Caballo.dado_de_baja == False)
    if nombre:
        query = query.filter(Caballo.nombre.ilike(f"%{nombre}%"))
    
    if tipo_ja_asignado:
        query = query.filter(Caballo.tipo_ja_asignado.ilike(f"%{tipo_ja_asignado}%"))  

    sort_column = getattr(Caballo, sort_by, Caballo.nombre)
    query = query.order_by(asc(sort_column) if order == 'asc' else desc(sort_column))

    return query.paginate(page=page, per_page=per_page, error_out=False)

def create_caballo(entrenadores_ids=None, conductores_ids=None, **kwargs):
    """
    Crea un nuevo caballo con entrenadores y conductores opcionales.

    Args:
        entrenadores_ids (list[int], optional): Lista de IDs de empleados que serán entrenadores.
        conductores_ids (list[int], optional): Lista de IDs de empleados que serán conductores.
        **kwargs: Atributos del caballo a crear.

    Returns:
        Caballo: El caballo creado.
    """
    
    caballo = Caballo(**kwargs)
    
    if entrenadores_ids:
        entrenadores = Empleado.query.filter(Empleado.id.in_(entrenadores_ids)).all()
        caballo.entrenadores.extend(entrenadores)
    
    if conductores_ids:
        conductores = Empleado.query.filter(Empleado.id.in_(conductores_ids)).all()
        caballo.conductores.extend(conductores)
    
    db.session.add(caballo)
    db.session.commit()
    return caballo

def get_caballo_by_id(id):
    """
    Obtiene un caballo por su ID.

    Args:
        id (int): ID del caballo a obtener.

    Returns:
        Caballo: El caballo obtenido.
    """
    caballo = Caballo.query.filter_by(id=id, dado_de_baja=False).first()
    if caballo is None:
        abort(404)
    return caballo

def update_caballo(id, **kwargs):
    """
    Actualiza un caballo existente.

    Args:
        id (int): ID del caballo a actualizar.
        **kwargs: Atributos del caballo a actualizar.

    Returns:
        Caballo: El caballo actualizado.
    """
    caballo = get_caballo_by_id(id)
    for key, value in kwargs.items():
        setattr(caballo, key, value)
    db.session.commit()
    return caballo

def delete_caballo(id):
    """
    Elimina un caballo por su ID.

    Args:
        id (int): ID del caballo a eliminar.
    """
    caballo = get_caballo_by_id(id)
    caballo.dado_de_baja = True
    db.session.commit()

def list_documents(caballo_id, nombre_documento=None, tipo_documento=None, sort_by='nombre_documento', order='asc', page=1, per_page=10):
    """
    Lista y busca documentos asociados a un caballo con filtros opcionales y paginación.

    Args:
        caballo_id (int): ID del caballo cuyos documentos se buscan.
        nombre_documento (str, optional): Nombre del documento para filtrar.
        tipo_documento (str, optional): Tipo de documento para filtrar.
        sort_by (str, optional): Columna por la cual ordenar los resultados. Por defecto es 'nombre_documento'.
        order (str, optional): Orden de la columna ('asc' para ascendente, 'desc' para descendente). Por defecto es 'asc'.
        page (int, optional): Número de página para la paginación. Por defecto es 1.
        per_page (int, optional): Número de elementos por página. Por defecto es 10.

    Returns:
        Pagination: Objeto de paginación con los documentos filtrados y ordenados.
    """
    query = Documento.query.filter(Documento.caballo_id == caballo_id)
    
    if nombre_documento:
        query = query.filter(Documento.nombre_documento.ilike(f"%{nombre_documento}%"))
    if tipo_documento:
        query = query.filter(Documento.tipo_documento.ilike(f"%{tipo_documento}%"))

    sort_column = getattr(Documento, sort_by, Documento.nombre_documento)
    query = query.order_by(asc(sort_column) if order == 'asc' else desc(sort_column))

    return query.paginate(page=page, per_page=per_page, error_out=False)

def update_document(document_id, **kwargs):
    """
    Actualiza un documento existente en la base de datos.

    Args:
        document_id: ID del documento a actualizar.
        **kwargs: Nuevos atributos del documento.

    Returns:
        Documento: El documento actualizado.
    """
    document = get_document_by_id(document_id)

    for key, value in kwargs.items():
        setattr(document, key, value)

    db.session.commit()
    return document

def delete_document(document_id):
    """
    Elimina un documento de la base de datos.

    Args:
        document_id: ID del documento a eliminar.
    """
    db.session.query(Documento).filter(Documento.id == str(document_id)).delete()
    db.session.commit()

def get_document_by_id(documento_id):
    """
    Obtiene un documento por su ID.

    Args:
        documento_id (int): ID del documento a obtener.

    Returns:
        Documento: El documento obtenido.
    """
    return Documento.query.get_or_404(documento_id)

def save_document(**kwargs):
    """
    Guarda un nuevo documento en la base de datos.

    Args:
        **kwargs: Atributos del documento a guardar.
    """
    document = Documento(**kwargs)
    db.session.add(document)
    db.session.commit()

def get_caballo_by_document(document):
    """
    Busca el caballo asociado a un documento.

    Args:
        document: El documento del cual se busca el caballo.

    Returns:
        Caballo or None: Retorna el objeto caballo encontrado o None si no existe.
    """
    caballo = Caballo.query.filter_by(id=document.caballo_id, dado_de_baja=False).first()
    return caballo


def get_empleados_by_rol(puesto):
    """
    Obtiene una lista de empleados por su rol.

    Args:
        rol (str): Rol del empleado (e.g., 'entrenador', 'conductor').

    Returns:
        list[Empleado]: Lista de empleados con el rol especificado.
    """
    
    return Empleado.query.filter_by(puesto=puesto).filter(Empleado.estado == True).all()


def get_empleados_by_ids(ids):
    """
    Recupera los empleados por su lista de IDs.
    """
 
 

    return Empleado.query.filter(Empleado.id.in_(ids), Empleado.estado == True).all()