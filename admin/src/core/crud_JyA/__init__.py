from core import db
from src.core.auth.models.model_JyA import JYA

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

def delete_jya(jya_dni):
    db.session.query(JYA).filter(JYA.dni==str(jya_dni)).delete()
    db.session.commit()
    
def get_jya_by_dni(dni):
    dni = str(dni)
    jya = JYA.query.filter_by(dni=dni).first()
    
    return jya