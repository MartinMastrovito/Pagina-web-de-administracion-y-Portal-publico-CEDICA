from src.core.database import db
from src.core.auth.models.model_JyA import JYA
from src.core.auth.models.model_documento import Documento
from src.core.auth.models.model_empleado import Empleados
from src.core.auth.models.model_caballos import Caballo
from src.core.auth.models.model_JYAEmpleado import JYAEmpleado
from sqlalchemy import or_
from flask import current_app

def list_users():
    """
    Devuelve la lista de todos los JYA.

    Returns:
        Lista de objetos JYA.
    """
    jya = JYA.query.all()
    return jya

def search_JYA(nombre=None, apellido=None, dni=None, profesionales_atendiendo=None, 
               sort_by='nombre', order='asc', page=1, per_page=10):
    """
    Busca JYA con filtros y devuelve una paginación de resultados.

    Args:
        nombre: Nombre del JYA.
        apellido: Apellido del JYA.
        dni: DNI del JYA.
        profesionales_atendiendo: Profesionales que están atendiendo al JYA.
        sort_by: Campo por el cual ordenar los resultados. Por defecto es 'nombre'.
        order: Orden de la lista ('asc' o 'desc'). Por defecto es 'asc'.
        page: Número de página a obtener. Por defecto es 1.
        per_page: Número de resultados por página. Por defecto es 25.

    Returns:
        Objeto de paginación con los resultados de la búsqueda.
    """
    query = JYA.query.filter_by(eliminado=False)

    if nombre:
        query = query.filter(JYA.nombre.ilike(f"%{nombre}%"))

    if apellido:
        query = query.filter(JYA.apellido.ilike(f"%{apellido}%"))

    if dni is not None:
        query = query.filter(JYA.dni.ilike(f"%{dni}%"))

    if profesionales_atendiendo:
        query = query.filter(JYA.profesionales_atendiendo.ilike(f"%{profesionales_atendiendo}%"))

    sort_column = {
        'nombre': JYA.nombre,
        'apellido': JYA.apellido,
        'dni': JYA.dni
    }.get(sort_by, JYA.nombre)

    if order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.paginate(page=page, per_page=per_page, error_out=False)

def create_jya(caballo_id, **kwargs):
    """
    Crea un nuevo JYA en la base de datos.

    Args:
        **kwargs: Atributos del JYA a crear.

    Returns:
        JYA or None: Retorna el objeto JYA creado o None si ya existe un JYA con el mismo DNI.
    """
    existing_jya = get_jya_by_dni(kwargs["dni"])
    if existing_jya:
        return None

    jya = JYA(**kwargs)
    
    caballo = Caballo.query.get(caballo_id)
    jya.caballo = caballo
    jya.caballo_id = caballo_id

    db.session.add(jya)
    db.session.commit()

    return jya

def assign_employee_to_jya(jya_id, empleado_id, rol):
    """
    Asigna un empleado a un JYA con un rol específico si no existe previamente.

    Args:
        jya_id: ID del JYA.
        empleado_id: ID del empleado a asignar.
        rol: Rol del empleado (terapeuta, conductor, auxiliar).
    """
    
    existente = JYAEmpleado.query.filter_by(jya_id=jya_id, rol=rol).first()

    if existente:
        if existente.empleado_id == empleado_id:
            return
        else:
            db.session.delete(existente)
            db.session.commit()
    
    asignacion = JYAEmpleado(
        jya_id=jya_id,
        empleado_id=empleado_id,
        rol=rol
    )
    db.session.add(asignacion)
    db.session.commit()

def update_jya(jya_dni, caballo_id, **kwargs):
    """
    Actualiza los datos de un JYA existente.

    Args:
        jya_dni: DNI del JYA a actualizar.
        **kwargs: Nuevos atributos del JYA.

    Returns:
        Retorna True si la actualización fue exitosa, o None si ya existe un JYA con el mismo DNI.
    """
    jya = get_jya_by_dni(jya_dni)
    validation = JYA.query.filter_by(dni=kwargs["dni"]).first()

    if validation and (not (jya.dni == kwargs["dni"])):
        return None

    caballo = Caballo.query.get(caballo_id)
    jya.caballo = caballo
    jya.caballo_id = caballo_id
    
    for key, value in kwargs.items():
        setattr(jya, key, value)

    db.session.commit()
    return True

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

def delete_jya(jya_dni):
    """
    Elimina un JYA y todos sus documentos del almacenamiento y la base de datos.

    Args:
        jya_dni: DNI del JYA a eliminar.
    """

    jya = get_jya_by_dni(jya_dni)

    if not jya:
        raise ValueError("El JYA especificado no existe.")

    documentos = get_documents_by_jya_dni(jya.dni)

    client = current_app.storage.client
    for documento in documentos:
        if documento.nombre_documento.startswith("documentos-JYA/"):
            client.remove_object("grupo30", documento.nombre_documento)
            
        delete_document(documento.id)

    db.session.query(JYAEmpleado).filter_by(jya_id=jya.id).delete(synchronize_session=False)

    jya.eliminado = True
    db.session.commit()

    
def delete_document(document_id):
    """
    Elimina un documento de la base de datos.

    Args:
        document_id: ID del documento a eliminar.
    """
    db.session.query(Documento).filter(Documento.id == str(document_id)).delete()
    db.session.commit()
    
def get_documents_by_jya_dni(jya_dni):
    """
    Recupera todos los documentos asociados a un JYA específico.

    Args:
        jya_id: ID del JYA cuyos documentos se desean recuperar.

    Returns:
        Una lista de objetos Documento asociados al JYA.
    """
    documentos = db.session.query(Documento).filter_by(jya_dni=jya_dni).all()
    return documentos

    
def get_jya_by_dni(dni):
    """
    Busca un JYA por su DNI.

    Args:
        dni: DNI del JYA a buscar.

    Returns:
        JYA or None: Retorna el objeto JYA encontrado o None si no existe.
    """
    dni = str(dni)
    jya = JYA.query.filter_by(dni=dni).first()
    return jya

def save_document(**kwargs):
    """
    Guarda un nuevo documento en la base de datos.

    Args:
        **kwargs: Atributos del documento a guardar.
    """
    document = Documento(**kwargs)
    db.session.add(document)
    db.session.commit()
    
def search_documents(jya_dni, nombre_documento=None, tipo_documento=None, 
                     sort_by='nombre_documento', order='asc', page=1, per_page=10):
    """
    Busca documentos asociados a un JYA.

    Args:
        jya_dni: DNI del JYA al que pertenecen los documentos.
        nombre_documento: Nombre del documento a buscar.
        tipo_documento: Tipo del documento a buscar.
        sort_by: Campo por el cual ordenar los resultados. Por defecto es 'nombre_documento'.
        order: Orden de la lista ('asc' o 'desc'). Por defecto es 'asc'.
        page: Número de página a obtener. Por defecto es 1.
        per_page): Número de resultados por página. Por defecto es 10.

    Returns:
        Objeto de paginación con los resultados de la búsqueda.
    """
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
    """
    Busca un documento por su ID.

    Args:
        document_id: ID del documento a buscar.

    Returns:
        El documento encontrado.
    """
    document = Documento.query.get_or_404(document_id)
    return document

def get_jya_by_document(document):
    """
    Busca el JYA asociado a un documento.

    Args:
        document: El documento del cual se busca el JYA.

    Returns:
        JYA or None: Retorna el objeto JYA encontrado o None si no existe.
    """
    jya = JYA.query.filter_by(dni=document.jya_dni).first()
    return jya

def get_empleados_terapeuta_profesor():
    """
    Devuelve todos los empleados que son terapeutas o profesores.

    Returns:
        Lista de empleados con profesión terapeuta o profesor.
    """
    empleados = Empleados.query.filter(
        or_(Empleados.puesto == "Terapeuta", Empleados.puesto == "Profesor")
    ).filter_by(estado=True).all()

    return empleados

def get_empleados_conductor():
    """
    Devuelve todos los empleados que son conductores.

    Returns:
        list: Lista de empleados con profesión conductor.
    """
    empleados = Empleados.query.filter_by(puesto="Conductor").filter_by(estado=True).all()
    return empleados
    
def get_empleados_auxiliar():
    """
    Devuelve todos los empleados que son auxiliares.

    Returns:
        list: Lista de empleados con profesión auxiliar.
    """
    empleados = Empleados.query.filter_by(puesto="Auxiliar de pista").filter_by(estado=True).all()
    return empleados

def get_caballos():
    """
    Devuelve la lista de todos los caballos.

    Returns:
        list: Lista de objetos Caballo.
    """
    caballos = Caballo.query.filter_by(dado_de_baja=False).all()
    return caballos

def get_jyaempleados_id(jya):
    """
    Obtiene los empleados asignados a un JYA y los clasifica por rol.

    Args:
        jya : el JYA para el cual se desean obtener los empleados asignados.

    Returns:
        dict: Un diccionario con los roles como claves ('profesor', 'terapeuta', 
              'conductor', 'auxiliar') y los valores correspondientes a los 
              IDs de los empleados asignados a cada rol.
    """
    jya_empleados = db.session.query(JYAEmpleado).filter(JYAEmpleado.jya_id == jya.id).all()
    
    empleados_por_rol = {
        'profesor': None,
        'terapeuta': None,
        'conductor': None,
        'auxiliar': None
    }

    for jya_empleado in jya_empleados:
        empleados_por_rol[jya_empleado.rol] = jya_empleado.empleado_id
        
    return empleados_por_rol

def get_jyaempleados(jya):
    """
    Obtiene los empleados asignados a un JYA y los clasifica por rol.

    Args:
        jya : el JYA para el cual se desean obtener los empleados asignados.

    Returns:
        dict: Un diccionario con los roles como claves ('profesor', 'terapeuta', 
              'conductor', 'auxiliar') y JYAEmpleado correspondientes a los 
              IDs de los empleados asignados a cada rol.
    """
    jya_empleados = db.session.query(JYAEmpleado).filter(JYAEmpleado.jya_id == jya.id).all()
    
    empleados_por_rol = {
        'profesor': None,
        'terapeuta': None,
        'conductor': None,
        'auxiliar': None
    }

    for jya_empleado in jya_empleados:
        empleados_por_rol[jya_empleado.rol] = jya_empleado
        
    return empleados_por_rol

def cant_documentos():
    '''
        Retorna la cantidad de documentos en total de todos los JYA
    '''
    return len(Documento.query.all())