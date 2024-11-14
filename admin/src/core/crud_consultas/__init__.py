from src.core.database import db
from src.core.auth.models.model_consulta import Consulta
from sqlalchemy import asc, desc

def search_consultas(nombre_completo=None, estado=None, sort_by='fecha', order='asc', page=1, per_page=10):
    query = Consulta.query

    if nombre_completo:
        query = query.filter(Consulta.nombre_completo.ilike(f"%{nombre_completo}%"))
    
    if estado:
        query = query.filter(Consulta.estado.ilike(f"%{estado}%"))

    sort_column = getattr(Consulta, sort_by, Consulta.fecha)
    query = query.order_by(asc(sort_column) if order == 'asc' else desc(sort_column))

    return query.paginate(page=page, per_page=per_page, error_out=False)

def create_consulta(**kwargs):
    consulta = Consulta(**kwargs)
    db.session.add(consulta)
    db.session.commit()
    return consulta

def get_consulta_by_id(id):
    return Consulta.query.get_or_404(id)

def update_consulta(id, **kwargs):
    consulta = get_consulta_by_id(id)
    for key, value in kwargs.items():
        setattr(consulta, key, value)
    db.session.commit()
    return consulta

def delete_consulta(id):
    consulta = get_consulta_by_id(id)
    db.session.delete(consulta)
    db.session.commit()
