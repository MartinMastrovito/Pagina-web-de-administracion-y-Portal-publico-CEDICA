from src.core.bcrypt import bcrypt
from src.core.database import db
from src.core.auth.models.model_user import User
from src.core.auth.models.model_permission import RolePermission, Permission

def get_permissions(user_id):
    """
    Obtiene los permisos asociados al rol de un usuario.

    Args:
        user_id: ID del usuario cuyas permisos se quieren obtener.

    Returns:
        Lista de nombres de permisos asociados al rol del usuario.
    """
    user = get_user(user_id)
    role_permissions = (
        db.session.query(Permission.name)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .filter(RolePermission.role_id == user.role_id)
        .all()
    )
    return [perm.name for perm in role_permissions]

def list_users():
    """
    Lista todos los usuarios en la base de datos.

    Returns:
        Lista de instancias de User.
    """
    users = User.query.all()
    return users

def search_users(email=None, enabled=None, role_id=None, sort_by='email', order='asc', page=1, per_page=10):
    """
    Busca usuarios en la base de datos aplicando varios filtros.

    Args:
        email: Email del usuario a buscar.
        enabled: Estado activo/inactivo del usuario.
        role_id: ID del rol del usuario a buscar.
        sort_by: Columna por la que ordenar (por defecto es 'email').
        order: Orden de la lista ('asc' o 'desc').
        page: Página de resultados (por defecto es 1).
        per_page: Número de resultados por página (por defecto es 25).

    Returns:
        Objeto de paginación con los usuarios encontrados.
    """
    query = User.query.filter_by(eliminado=False)
    
    query = query.filter(User.role_id.isnot(None))

    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    if enabled is not None and enabled != '':
        is_enabled = True if enabled.lower() == 'si' else False
        query = query.filter_by(enabled=is_enabled)

    if role_id is not None and role_id != '':
        query = query.filter_by(role_id=role_id)
        
    if sort_by == 'email':
        sort_column = User.email
    elif sort_by == "created_at":
        sort_column = User.created_at
    else:
        sort_column = User.email

    if order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.paginate(page=page, per_page=per_page, error_out=False)

def search_unaccepted_users(email=None, order='asc', page=1, per_page=10):
    """
    Busca usuarios no aceptados en la base de datos aplicando varios filtros.

    Args:
        email: Email del usuario a buscar.
        order: Orden de la lista ('asc' o 'desc').
        page: Página de resultados (por defecto es 1).
        per_page: Número de resultados por página (por defecto es 25).

    Returns:
        Objeto de paginación con los usuarios encontrados.
    """

    query = User.query.filter(User.role_id.is_(None))

    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    sort_column = User.email

    if order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.paginate(page=page, per_page=per_page, error_out=False)

def create_user(**kwargs):
    """
    Crea un nuevo usuario en la base de datos.

    Args:
        **kwargs: Argumentos que representan los datos del nuevo usuario.

    Returns:
        Instancia del nuevo usuario si se creó exitosamente, None si ya existe.
    """
    existing_user = get_user_by_email(kwargs["email"])
    if existing_user:
        return None  # Retorna None si el usuario ya existe
    
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs["password"] = hash.decode("utf-8")
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def create_google_user(email, alias):
    """
    Crea un nuevo usuario en la base de datos mediante las credenciales de google.

    Args:
        **kwargs: Argumentos que representan los datos del nuevo usuario.
    """

    user = User(email=email, alias=alias, enabled=False)
    db.session.add(user)
    db.session.commit()

def get_user(user_id):
    """
    Obtiene un usuario de la base de datos por su ID.

    Args:
        user_id: ID del usuario a obtener.

    Returns:
        Instancia del usuario.
    """
    return User.query.get_or_404(user_id)

def update_user(user_id, **kwargs):
    """
    Actualiza los datos de un usuario en la base de datos.

    Args:
        user_id: ID del usuario a actualizar.
        **kwargs: Argumentos que representan los nuevos datos del usuario.

    Returns:
        str or False: Mensaje de error si el email ya está en uso, False si se actualizó correctamente.
    """
    validation = User.query.filter_by(email=kwargs["email"]).first()
    user = get_user(user_id)
    
    if (validation) and (not (user.email == kwargs["email"])):
        return "Este email está siendo utilizado, pruebe ingresar uno diferente."
    
    for key, value in kwargs.items():
        setattr(user, key, value)
    
    db.session.commit()
    
    return False

def accept_user(user_id, role_id):
    """
    Actualiza los datos de un usuario en la base de datos para aceptarlo.

    Args:
        user_id: ID del usuario a actualizar.
        user_data: Argumentos que representa el role_id del usuario.
    """
    user = get_user(user_id)
    
    user.role_id = role_id
    user.enabled = True
    
    db.session.commit()

def delete_user(user_id):
    """
    Elimina un usuario de la base de datos.

    Args:
        user_id: ID del usuario a eliminar.
    """
    user = get_user(user_id)
    if user and user.role_id != 6:
        user.eliminado = True
        block_user(user.id)
        db.session.commit()
        return True
    return False

def get_user_by_email(email):
    """
    Obtiene un usuario de la base de datos por su email.

    Args:
        email: Email del usuario a buscar.

    Returns:
        User or None: Instancia del usuario si se encuentra, None si no.
    """
    return User.query.filter_by(email=email).first()

def login_user(email, password):
    """
    Valida las credenciales de un usuario para iniciar sesión.

    Args:
        email: Email del usuario.
        password: Contraseña del usuario.

    Returns:
        User or None: Instancia del usuario si las credenciales son válidas, None si no.
    """
    user = get_user_by_email(email)
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None

def block_user(user_id):
    """
    Bloquea un usuario en la base de datos.

    Args:
        user_id: ID del usuario a bloquear.

    Returns:
        bool: True si se bloqueó correctamente, False si no se pudo bloquear.
    """
    user = get_user(user_id)
    if user and user.role_id != 6:
        user.enabled = False
        db.session.commit()
        return True
    return False

def unblock_user(user_id):
    """
    Desbloquea un usuario en la base de datos.

    Args:
        user_id: ID del usuario a desbloquear.

    Returns:
        bool: True si se desbloqueó correctamente, False si no se pudo desbloquear.
    """
    user = get_user(user_id)
    if user:
        user.enabled = True
        db.session.commit()
        return True
    return False

def unaccepted_users():
    return User.query.filter(User.role_id.is_(None)).count()