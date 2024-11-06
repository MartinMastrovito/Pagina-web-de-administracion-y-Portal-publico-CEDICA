from src.core.database import db
from src.core.auth.models.model_caballos import Caballo
from src.core.auth.models.model_documento import Documento
from sqlalchemy import asc, desc
from werkzeug.utils import secure_filename
from minio import Minio
from minio.error import S3Error



def search_caballos(nombre=None, tipo_ja_asignado=None, sort_by='nombre', order='asc', page=1, per_page=10):
    query = db.session.query(Caballo)

    if nombre:
        query = query.filter(Caballo.nombre.ilike(f"%{nombre}%"))
    
    if tipo_ja_asignado:
        query = query.filter(Caballo.tipo_ja_asignado.ilike(f"%{tipo_ja_asignado}%"))  

    sort_column = getattr(Caballo, sort_by, Caballo.nombre)
    query = query.order_by(asc(sort_column) if order == 'asc' else desc(sort_column))

    return query.paginate(page=page, per_page=per_page, error_out=False)


def create_caballo(**kwargs):
    caballo = Caballo(**kwargs)
    db.session.add(caballo)
    db.session.commit()
    return caballo

def get_caballo_by_id(id):
    return Caballo.query.get_or_404(id)

def update_caballo(id, **kwargs):
    caballo = get_caballo_by_id(id)
    for key, value in kwargs.items():
        setattr(caballo, key, value)
    db.session.commit()
    return caballo

def delete_caballo(id):
    caballo = get_caballo_by_id(id)
    db.session.delete(caballo)
    db.session.commit()
#cumple la funcion de list and search
def list_documents(caballo_id, nombre_documento=None, tipo_documento=None, sort_by='nombre_documento', order='asc', page=1, per_page=10):
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
        El documento actualizado.
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
    document = Documento.query.get_or_404(documento_id)
    return document


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
        caballo or None: Retorna el objeto caballo encontrado o None si no existe.
    """
    caballo = Caballo.query.filter_by(id=document.caballo_id).first()
    return caballo

