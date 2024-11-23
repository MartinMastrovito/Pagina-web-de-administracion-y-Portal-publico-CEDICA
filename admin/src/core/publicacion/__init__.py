from src.core.database import db
from src.core.auth.models.model_publicacion import Publicacion
from datetime import datetime


def obtener_publicaciones(page, per_page):
    """
    Obtiene las publicaciones paginadas.

    Recupera las publicaciones de la base de datos, ordenadas por la fecha de actualización
    de manera ascendente y las devuelve en formato paginado.

    Args:
        page : Número de página para la paginación.
        per_page : Número de publicaciones por página.

    Returns:
        Pagination: Un objeto de tipo Pagination que contiene las publicaciones de la página
                    solicitada.
    """
    return Publicacion.query.order_by(Publicacion.fecha_actualizacion.asc()).paginate(page=page, per_page=per_page)

def crear_publicacion(kwargs):
    """
    Crea una nueva publicación en la base de datos.

    Utiliza los datos proporcionados en kwargs para crear una nueva instancia del modelo
    Publicacion, la agrega a la sesión y la guarda en la base de datos.

    Args:
        kwargs : Diccionario con los atributos de la nueva publicación.
    """
    pub = Publicacion(**kwargs)
    db.session.add(pub)
    db.session.commit()
    
def eliminar_publicacion(id):
    """
    Elimina una publicación de la base de datos.

    Busca la publicación por su ID, la elimina de la base de datos y confirma los cambios.

    Args:
        id : El ID de la publicación a eliminar.
    """
    publicacion = get_publicacion(id)
    db.session.delete(publicacion)
    db.session.commit()
    
def actualizar_publicacion(id, **kwargs):
    """
    Actualiza una publicación existente en la base de datos.

    Busca la publicación por su ID, actualiza sus atributos con los valores proporcionados
    en kwargs y confirma los cambios.

    Args:
        id : El ID de la publicación a actualizar.
        kwargs : Diccionario con los nuevos valores para los atributos de la publicación.
    """
    publicacion = Publicacion.query.filter_by(id=id).first()

    for key, value in kwargs.items():
        setattr(publicacion, key, value)

    db.session.commit()
    
def get_publicacion(id):
    """
    Obtiene una publicación por su ID.

    Busca y devuelve la publicación correspondiente al ID proporcionado.

    Args:
        id : El ID de la publicación a obtener.

    Returns:
        Publicacion : La publicación encontrada con el ID proporcionado.

    Raises:
        404 : Si no se encuentra la publicación con el ID proporcionado.
    """
    return Publicacion.query.get_or_404(id)

def filtrado_portal(**kwargs):
    titulo = kwargs.get('titulo')
    page = kwargs.get('page')
    per_page = kwargs.get('per_page')
    desde = kwargs.get('desde')
    hasta = kwargs.get('hasta')
    publicaciones = Publicacion.query.order_by(Publicacion.fecha_creacion.desc())
    if desde:
        desde = desde.strip('"')
        publicaciones = publicaciones.filter(Publicacion.fecha_creacion >= (desde))
    if titulo:
        publicaciones = publicaciones.filter(Publicacion.titulo.like(f"%{titulo}%"))
    if hasta:
        hasta = hasta.strip('"')
        hasta = datetime.strptime(hasta,"%Y-%m-%d").date()
        publicaciones = publicaciones.filter(Publicacion.fecha_creacion <= (hasta))
        
    publicaciones=publicaciones.paginate(page=page, per_page=per_page)

    return publicaciones
