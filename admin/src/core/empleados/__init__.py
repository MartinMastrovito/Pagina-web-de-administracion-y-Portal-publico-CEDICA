from src.core.database import db
from src.core.auth.models.model_empleado import Empleados
from src.core.auth.models.model_docEmpleado import DocumentoEmpleado
from sqlalchemy import or_

def lista_empleado():
    """
    Devuelve la lista de todos los empleados.

    Returns:
        Lista de objetos Empleado.
    """
    empleados = Empleados.query.all()
    return empleados

def buscar_empleado(nombre=None, apellido=None, dni=None, puesto=None, 
                     sort_by='nombre', order='asc', page=1, per_page=25):
    """
    Busca empleados con filtros y devuelve una paginación de resultados.

    Args:
        nombre: Nombre del empleado.
        apellido: Apellido del empleado.
        dni: DNI del empleado.
        puesto: Puesto del empleado.
        sort_by: Campo por el cual ordenar los resultados. Por defecto es 'nombre'.
        order: Orden de la lista ('asc' o 'desc'). Por defecto es 'asc'.
        page: Número de página a obtener. Por defecto es 1.
        per_page: Número de resultados por página. Por defecto es 25.

    Returns:
        Objeto de paginación con los resultados de la búsqueda.
    """
    query = Empleados.query

    if nombre:
        query = query.filter(Empleados.nombre.ilike(f"%{nombre}%"))

    if apellido:
        query = query.filter(Empleados.apellido.ilike(f"%{apellido}%"))

    if dni is not None:
        query = query.filter_by(dni=str(dni))

    if puesto:
        query = query.filter(Empleados.puesto.ilike(f"%{puesto}%"))

    sort_column = {
        'nombre': Empleados.nombre,
        'apellido': Empleados.apellido,
        'dni': Empleados.dni
    }.get(sort_by, Empleados.nombre)

    if order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.paginate(page=page, per_page=per_page, error_out=False)

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

def actualizar_empleado(dni, **kwargs):
    """
    Actualiza los datos de un empleado existente.

    Args:
        dni: DNI del empleado a actualizar.
        **kwargs: Nuevos atributos del empleado.

    Returns:
        Retorna True si la actualización fue exitosa, o None si ya existe un empleado con el mismo DNI.
    """
    empleado = get_empleado_por_dni(dni)
    validation = Empleados.query.filter_by(dni=kwargs["dni"]).first()

    if validation and (not (empleado.dni == kwargs["dni"])):
        return None

    for key, value in kwargs.items():
        setattr(empleado, key, value)

    db.session.commit()
    return True

def eliminar_empleado(dni):
    """
    Elimina un empleado de la base de datos.

    Args:
        dni: DNI del empleado a eliminar.
    """
    empleado = get_empleado_por_dni(dni)
    db.session.delete(empleado)
    db.session.commit()

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

def guardar_documento(**kwargs):
    """
    Guarda un nuevo documento en la base de datos.

    Args:
        **kwargs: Atributos del documento a guardar.
    """
    document = DocumentoEmpleado(**kwargs)
    db.session.add(document)
    db.session.commit()

def search_documents(empleado_dni, nombre_documento=None, tipo_documento=None, 
                     sort_by='nombre_documento', order='asc', page=1, per_page=10):
    """
    Busca documentos asociados a un empleado.

    Args:
        empleado_dni: DNI del empleado al que pertenecen los documentos.
        nombre_documento: Nombre del documento a buscar.
        tipo_documento: Tipo del documento a buscar.
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

    if tipo_documento:
        query = query.filter(DocumentoEmpleado.tipo_documento.ilike(f'%{tipo_documento}%'))

    if order == 'desc':
        query = query.order_by(getattr(DocumentoEmpleado, sort_by).desc())
    else:
        query = query.order_by(getattr(DocumentoEmpleado, sort_by))

    return query.paginate(page=page, per_page=per_page)

def search_empleados(nombre=None, apellido=None, dni=None, email=None, sort_by='nombre', order='asc', page=1, per_page=10):
    """
    Busca empleados en la base de datos aplicando filtros y ordenación.

    Args:
        nombre (str): Nombre del empleado.
        apellido (str): Apellido del empleado.
        dni (str): DNI del empleado.
        email (str): Email del empleado.
        sort_by (str): Columna por la que ordenar ('nombre', 'apellido', 'dni', etc.).
        order (str): Dirección de la ordenación ('asc' o 'desc').
        page (int): Página actual.
        per_page (int): Número de resultados por página.

    Returns:
        Pagination: Objeto de paginación con los resultados.
    """
    query = Empleados.query

    if nombre:
        query = query.filter(Empleados.nombre.ilike(f"%{nombre}%"))
    if apellido:
        query = query.filter(Empleados.apellido.ilike(f"%{apellido}%"))
    if dni:
        query = query.filter(Empleados.dni.ilike(f"%{dni}%"))
    if email:
        query = query.filter(Empleados.email.ilike(f"%{email}%"))

    sort_column = getattr(Empleados, sort_by, Empleados.nombre)
    if order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.paginate(page=page, per_page=per_page, error_out=False)