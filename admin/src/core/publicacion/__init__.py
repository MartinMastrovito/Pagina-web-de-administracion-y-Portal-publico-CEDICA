from src.core.database import db
from src.core.auth.models.model_publicacion import Publicacion
from src.core.empleados import get_empleado_by_id
from datetime import datetime

def obtener_publicaciones(estado=None, sort_by='fecha_actualizacion', order='desc', page=1, per_page=10):
    """
    Obtiene las publicaciones paginadas.

    Recupera las publicaciones de la base de datos, ordenadas según la columna y el orden
    especificados, y las devuelve en formato paginado.

    Args:
        estado (str, optional): Estado para filtrar las consultas.
        sort_by (str): Columna por la cual ordenar las publicaciones.
        order (str): Orden de la columna ('asc' para ascendente, 'desc' para descendente).
        page (int): Número de página para la paginación.
        per_page (int): Número de publicaciones por página.

    Returns:
        Pagination: Un objeto de tipo Pagination con las publicaciones de la página solicitada.
    """
    query = Publicacion.query

    if estado:
        query = query.filter(Publicacion.estado == estado)

    sort_columns = {
        'fecha_actualizacion': Publicacion.fecha_actualizacion,
        'fecha_creacion': Publicacion.fecha_creacion,
    }

    sort_column = sort_columns.get(sort_by, Publicacion.fecha_actualizacion)

    if order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.paginate(page=page, per_page=per_page, error_out=False)

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

    empleado = get_empleado_by_id(kwargs["autor_id"])
    publicacion.nombre_autor = f"{empleado.nombre} {empleado.apellido}"

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
    publicaciones = Publicacion.query.filter(Publicacion.estado=='Publicado').order_by(Publicacion.fecha_creacion.desc())
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
