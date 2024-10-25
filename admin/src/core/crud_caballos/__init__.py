from src.core.database import db
from src.core.auth.models.model_caballos import Caballo
from src.core.auth.models.model_documento import Documento
from sqlalchemy import asc, desc
from werkzeug.utils import secure_filename
import os

def search_caballos(nombre=None, sort_by='nombre', order='asc', page=1, per_page=10):
    """Obtiene una lista paginada de caballos con filtros y ordenamiento."""
    query = db.session.query(Caballo)
    
    # Filtrar por nombre
    if nombre:
        query = query.filter(Caballo.nombre.ilike(f"%{nombre}%"))
    
    # Ordenar resultados
    sort_column = getattr(Caballo, sort_by, Caballo.nombre)
    if order == 'asc':
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    
    # Paginación
    return query.paginate(page=page, per_page=per_page, error_out=False)

def create_caballo(**kwargs):
    """Crea un nuevo caballo."""
    caballo = Caballo(**kwargs)
    db.session.add(caballo)
    db.session.commit()
    return caballo

def get_caballo_by_id(id):
    """Obtiene un caballo específico por su ID."""
    return Caballo.query.get_or_404(id)

def update_caballo(id, **kwargs):
    """Actualiza la información de un caballo."""
    caballo = get_caballo_by_id(id)
    for key, value in kwargs.items():
        setattr(caballo, key, value)
    db.session.commit()
    return caballo

def delete_caballo(id):
    """Elimina un caballo por su ID."""
    caballo = get_caballo_by_id(id)
    db.session.delete(caballo)
    db.session.commit()

def list_documents(caballo_id, nombre=None, tipo=None, sort_by='nombre', order='asc', page=1, per_page=10):
    """Lista documentos asociados a un caballo, con filtros y paginación."""
    query = Documento.query.filter(Documento.caballo_id == caballo_id)
    
    if nombre:
        query = query.filter(Documento.nombre.ilike(f"%{nombre}%"))
    if tipo:
        query = query.filter(Documento.tipo_documento.ilike(f"%{tipo}%"))

    sort_column = getattr(Documento, sort_by, Documento.nombre_documento)
    query = query.order_by(asc(sort_column) if order == 'asc' else desc(sort_column))

    return query.paginate(page=page, per_page=per_page, error_out=False)

def upload_document(caballo_id, archivo, nombre_documento, tipo_documento):
    """Sube un documento y lo asocia a un caballo."""
    filename = secure_filename(archivo.filename)
    file_path = os.path.join('src/static/uploads', filename)  # Define tu ruta para guardar los archivos
    archivo.save(file_path)

    nuevo_documento = Documento(
        nombre=nombre_documento,
        tipo_documento=tipo_documento,
        archivo_url=file_path,
        caballo_id=caballo_id
    )
    db.session.add(nuevo_documento)
    db.session.commit()

def delete_document(id):
    """Elimina un documento por su ID."""
    documento = Documento.query.get_or_404(id)
    db.session.delete(documento)
    db.session.commit()
