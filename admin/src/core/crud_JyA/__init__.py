from src.core.database import db
from src.core.auth.models.model_JyA import JYA
from src.core.auth.models.model_documento import Documento

def list_users():
    jya = JYA.query.all()

    return jya

def search_JYA(nombre=None, apellido=None, dni=None, profesionales_atendiendo=None, sort_by='nombre', order='asc', page=1, per_page=25):
    query = JYA.query

    # Filtro por nombre
    if nombre:
        query = query.filter_by(nombre=nombre)

    # Filtro por apellido
    if apellido:
        query = query.filter_by(apellido=apellido)
    
    # Filtro por dni
    if dni is not None:
        query = query.filter_by(dni=str(dni))
        
    if profesionales_atendiendo:
        query = query.filter(JYA.profesionales_atendiendo.ilike(f"%{profesionales_atendiendo}%"))

    # Ordenación
    if sort_by == 'nombre':
        sort_column = JYA.nombre
    elif sort_by == "apellido":
        sort_column = JYA.apellido
    elif sort_by == "dni":
        sort_column = JYA.dni
    else:
        sort_column = JYA.nombre

    if order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # Paginación
    return query.paginate(page=page, per_page=per_page, error_out=False)

def create_jya(**kwargs):
    
    existing_jya = get_jya_by_dni(kwargs["dni"])
    if existing_jya:
        return None  # Retorna None si el usuario ya existe

    jya = JYA(**kwargs)
    db.session.add(jya)
    db.session.commit()

    return jya

def update_jya(jya_dni, **kwargs):
    jya = get_jya_by_dni(jya_dni)
    
    # Actualizar los atributos del usuario con los valores proporcionados en kwargs
    for key, value in kwargs.items():
        setattr(jya, key, value)
    
    # Confirmar los cambios en la base de datos
    db.session.commit()
    
    return jya

def update_document(document_id, **kwargs):
    document = get_document_by_id(document_id)
    
    for key, value in kwargs.items():
        setattr(document, key, value)
    
    # Confirmar los cambios en la base de datos
    db.session.commit()
    
    return document

def delete_jya(jya_dni):
    db.session.query(JYA).filter(JYA.dni==str(jya_dni)).delete()
    db.session.commit()
    
def delete_document(document_id):
    db.session.query(Documento).filter(Documento.id==str(document_id)).delete()
    db.session.commit()
    
def get_jya_by_dni(dni):
    dni = str(dni)
    jya = JYA.query.filter_by(dni=dni).first()
    
    return jya

def save_document(**kwargs):
    document = Documento(**kwargs)
    db.session.add(document)
    db.session.commit()
    
def search_documents(jya_dni, nombre_documento=None, tipo_documento=None, sort_by='nombre_documento', order='asc', page=1, per_page=10):
    query = Documento.query.filter(Documento.jya_dni == str(jya_dni))

    if nombre_documento:
        query = query.filter(Documento.nombre_documento.ilike(f'%{nombre_documento}%'))
    
    if tipo_documento:
        query = query.filter(Documento.tipo_documento.ilike(f'%{tipo_documento}%'))

    if order == 'desc':
        query = query.order_by(getattr(Documento, sort_by).desc())
    else:
        query = query.order_by(getattr(Documento, sort_by))

    return query.paginate(page=page, per_page=per_page)

def get_document_by_id(document_id):
    document = Documento.query.get_or_404(document_id)

    return document

def get_jya_by_document(document):
    jya = JYA.query.filter_by(dni=document.jya_dni).first()
    
    return jya