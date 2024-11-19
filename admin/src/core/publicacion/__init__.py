from sqlalchemy import func
from src.core.database import db
from src.core.auth.models.model_publicacion import Publicacion


def obtener_publicaciones(page, per_page):
    
    return Publicacion.query.order_by(Publicacion.fecha_actualizacion.asc()).paginate(page=page, per_page=per_page)

def crear_publicacion(kwargs):
    pub = Publicacion(**kwargs)
    db.session.add(pub)
    db.session.commit()
    
def eliminar_publicacion(id):
    publicacion = get_publicacion(id)
    db.session.delete(publicacion)
    db.session.commit()
    
def actualizar_publicacion(id, **kwargs):
    publicacion = Publicacion.query.filter_by(id=id).first()

    for key, value in kwargs.items():
        setattr(publicacion, key, value)

    db.session.commit()
    
def get_publicacion(id):
    return Publicacion.query.get_or_404(id)