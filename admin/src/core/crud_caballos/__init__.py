from src.core.database import db
from src.core.auth.models.model_caballos import Caballo
from src.core.auth.models.model_documento import Documento
from sqlalchemy import asc, desc
from werkzeug.utils import secure_filename
from minio import Minio
from minio.error import S3Error

# Configura tu cliente de MinIO
minio_client = Minio(
    "MINIO_ENDPOINT",
    access_key="MINIO_ACCESS_KEY",
    secret_key="MINIO_SECRET_KEY",
    secure=True  # Cambia a True si usas HTTPS
)

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

def list_documents(caballo_id, nombre_documento=None, tipo_documento=None, sort_by='nombre_documento', order='asc', page=1, per_page=10):
    query = Documento.query.filter(Documento.caballo_id == caballo_id)
    
    if nombre_documento:
        query = query.filter(Documento.nombre_documento.ilike(f"%{nombre_documento}%"))
    if tipo_documento:
        query = query.filter(Documento.tipo_documento.ilike(f"%{tipo_documento}%"))

    sort_column = getattr(Documento, sort_by, Documento.nombre_documento)
    query = query.order_by(asc(sort_column) if order == 'asc' else desc(sort_column))

    return query.paginate(page=page, per_page=per_page, error_out=False)

def upload_document(caballo_id, archivo, nombre_documento, tipo_documento):
    filename = secure_filename(archivo.filename)
    file_path = f"{caballo_id}/{filename}"  # Define el path en MinIO
    minio_client.put_object("nombre_bucket", file_path, archivo, archivo.content_length)
    
    nuevo_documento = Documento(
        nombre_documento=nombre_documento,
        tipo_documento=tipo_documento,
        archivo_url=f"URL_DE_MINIO/nombre_bucket/{file_path}",
        caballo_id=caballo_id
    )
    db.session.add(nuevo_documento)
    db.session.commit()

def update_document(documento_id, archivo=None, nombre_documento=None, tipo_documento=None):
    documento = Documento.query.get_or_404(documento_id)
    
    if archivo:
        filename = secure_filename(archivo.filename)
        file_path = f"{documento.caballo_id}/{filename}"  # Define el path en MinIO
        minio_client.put_object("nombre_bucket", file_path, archivo, archivo.content_length)
        documento.archivo_url = f"URL_DE_MINIO/nombre_bucket/{file_path}"
    
    if nombre_documento:
        documento.nombre_documento = nombre_documento
    if tipo_documento:
        documento.tipo_documento = tipo_documento
    
    db.session.commit()

def delete_document(documento_id):
    documento = Documento.query.get_or_404(documento_id)
    try:
        minio_client.remove_object("nombre_bucket", documento.archivo_url.split("/")[-1])
    except S3Error as e:
        print("Error al eliminar el documento de MinIO:", e)
    
    db.session.delete(documento)
    db.session.commit()

def get_document_by_id(documento_id):
    return Documento.query.get_or_404(documento_id)

