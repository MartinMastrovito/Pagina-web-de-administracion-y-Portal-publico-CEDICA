from src.core.database import db
from src.core.auth.models.model_empleado import Empleados
from src.core.auth.models.model_docEmpleado import DocumentoEmpleado

def get_empleados():
    return Empleados.query.filter_by(estado=True).all()

def listar_empleados_activos():
    return Empleados.query.filter_by(activo=True).all()

def lista_empleado():
    """
    Devuelve la lista de todos los empleados.

    Returns:
        Lista de objetos Empleado.
    """
    empleados = Empleados.query.all()
    return empleados

def crear_empleado(**kwargs):
    """
    Crea un nuevo empleado en la base de datos.

    Args:
        **kwargs: Atributos del empleado a crear.

    Returns:
        Empleado or None: Retorna el objeto Empleado creado o None si ya existe un empleado con el mismo DNI.
    """
    existing_empleado = get_empleado_por_dni(kwargs["dni"])
    if existing_empleado:
        return None

    empleado = Empleados(**kwargs)
    db.session.add(empleado)
    db.session.commit()

    return empleado

def actualizar_empleado(empleado_id, **kwargs):
    """
    Actualiza los datos de un empleado existente.

    Args:
        dni: DNI del empleado a actualizar.
        **kwargs: Nuevos atributos del empleado.

    Returns:
        Retorna True si la actualización fue exitosa, o None si ya existe un empleado con el mismo DNI.
    """
    empleado = Empleados.query.get(empleado_id)
    validation = Empleados.query.filter_by(dni=kwargs["dni"]).first()

    if validation and (not (empleado.dni == kwargs["dni"])):
        return None

    for key, value in kwargs.items():
        setattr(empleado, key, value)

    db.session.commit()
    return True

def eliminar_empleado(dni):
    """
    Elimina logico un empleado.

    Args:
        dni: DNI del empleado a eliminar.
    """
    empleado = get_empleado_por_dni(dni)
    if not empleado:
        return False
    empleado.estado = False  
    db.session.commit()
    return True

def get_empleado_por_dni(dni):
    """
    Busca un empleado por su DNI.

    Args:
        dni: DNI del empleado a buscar.

    Returns:
        Empleado o None: Retorna el objeto Empleado encontrado o None si no existe.
    """
    dni = str(dni)
    empleado = Empleados.query.filter_by(dni=dni).first()
    return empleado

def get_empleado_by_id(id):
    """
    Busca un empleado por su ID.

    Args:
        id: ID del empleado a buscar.

    Returns:
        Empleado o None: Retorna el objeto Empleado encontrado o None si no existe.
    """
    empleado = Empleados.query.get(id)
    return empleado

def guardar_documento(**kwargs):
    """
    Guarda un nuevo documento en la base de datos.

    Args:
        **kwargs: Atributos del documento a guardar.
    """
    document = DocumentoEmpleado(**kwargs)
    db.session.add(document)
    db.session.commit()

def search_documents(empleado_dni, nombre_documento=None, sort_by='nombre_documento', order='asc', page=1, per_page=10):
    """
    Busca documentos asociados a un empleado.

    Args:
        empleado_dni: DNI del empleado al que pertenecen los documentos.
        nombre_documento: Nombre del documento a buscar.
        sort_by: Campo por el cual ordenar los resultados. Por defecto es 'nombre_documento'.
        order: Orden de la lista ('asc' o 'desc'). Por defecto es 'asc'.
        page: Número de página a obtener. Por defecto es 1.
        per_page: Número de resultados por página. Por defecto es 10.

    Returns:
        Objeto de paginación con los resultados de la búsqueda.
    """
    query = DocumentoEmpleado.query.filter(DocumentoEmpleado.empleado_dni == str(empleado_dni))

    if nombre_documento:
        query = query.filter(DocumentoEmpleado.nombre_documento.ilike(f'%{nombre_documento}%'))

    sort_column = getattr(DocumentoEmpleado, sort_by, DocumentoEmpleado.nombre_documento)
    if order == 'desc':
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    return query.paginate(page=page, per_page=per_page)


def search_empleados(nombre=None, apellido=None, dni=None, email=None, puesto=None, sort_by='nombre', order='asc', page=1, per_page=10):
    """
    Busca empleados en la base de datos aplicando filtros y ordenación.

    Args:
        nombre (str): Nombre del empleado.
        apellido (str): Apellido del empleado.
        dni (str): DNI del empleado.
        email (str): Email del empleado.
        puesto (str): Puesto laboral del empleado.
        sort_by (str): Columna por la que ordenar ('nombre', 'apellido', 'dni', etc.).
        order (str): Dirección de la ordenación ('asc' o 'desc').
        page (int): Página actual.
        per_page (int): Número de resultados por página.

    Returns:
        Pagination: Objeto de paginación con los resultados.
    """
    query = db.session.query(Empleados).filter_by(estado=True)

    if nombre:
        query = query.filter(Empleados.nombre.ilike(f"%{nombre}%"))
    if apellido:
        query = query.filter(Empleados.apellido.ilike(f"%{apellido}%"))
    if dni:
        query = query.filter(Empleados.dni.ilike(f"%{dni}%"))
    if email:
        query = query.filter(Empleados.email.ilike(f"%{email}%"))
    if puesto:
        query = query.filter(Empleados.puesto == puesto)

    sort_column = getattr(Empleados, sort_by, Empleados.nombre)
    if order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.paginate(page=page, per_page=per_page, error_out=False)


def save_document(**kwargs):
    """
    Guarda un nuevo documento en la base de datos.

    Args:
        **kwargs: Atributos del documento a guardar.
    """
    document = DocumentoEmpleado(**kwargs)
    db.session.add(document)
    db.session.commit()
    
def get_document_by_id(document_id):
    """
    Busca un documento por su ID.

    Args:
        document_id: ID del documento a buscar.

    Returns:
        El documento encontrado.
    """
    document = DocumentoEmpleado.query.get_or_404(document_id)
    return document

def get_empleado_by_document(document):
    """
    Busca el empleado asociado a un documento.

    Args:
        document: El documento del cual se busca el empleado.

    Returns:
        empleado or None: Retorna el objeto empleado encontrado o None si no existe.
    """
    empleado = Empleados.query.filter_by(dni=document.empleado_dni).first()
    return empleado

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
    db.session.query(DocumentoEmpleado).filter(DocumentoEmpleado.id == str(document_id)).delete()
    db.session.commit()

def cant_documentos():
    '''
        Retorna la cantidad de documentos en total de todos los empleados
    '''
    return len(DocumentoEmpleado.query.all())