#aca se guardan todos los metodos que se van a usar en la base de datos
#como la comprobacion de login, por ejemplo
from core.bcrypt import bcrypt
from src.core.database import db
from core.auth.models.model_user import User , Role
from core.auth.models.model_permission import  RolePermission, Permission

def get_permissions(user_id):
    user = get_user(user_id)
    # Obtenemos los permisos asociados al rol del usuario
    role_permissions = (
        db.session.query(Permission.name)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .filter(RolePermission.role_id == user.role_id)
        .all()
    )
    # Devuelve una lista de nombres de permisos
    return [perm.name for perm in role_permissions]

def list_users():
    users = User.query.all()

    return users

def search_users(email=None, enabled=None, role_id=None, sort_by='email', order='asc', page=1, per_page=25):
    query = User.query

    # Filtro por email
    if email:
        query = query.filter_by(email=email)

    # Filtro por estado activo/inactivo
    if enabled is not None and enabled != '':
        is_enabled = True if enabled.lower() == 'si' else False
        query = query.filter_by(enabled=is_enabled)

    # Filtro por rol usando el ID
    if role_id is not None and role_id != '':
        query = query.filter_by(role_id=role_id)

    # Ordenación
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

    # Paginación
    return query.paginate(page=page, per_page=per_page, error_out=False)

def create_user(**kwargs):
    
    existing_user = get_user_by_email(kwargs["email"])
    if existing_user:
        return None  # Retorna None si el usuario ya existe
    
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs["password"] = hash.decode("utf-8")
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def get_user(user_id):
    return User.query.get_or_404(user_id)

def update_user(user_id, **kwargs):
    user = get_user(user_id)
    
    # Actualizar los atributos del usuario con los valores proporcionados en kwargs
    for key, value in kwargs.items():
        setattr(user, key, value)
    
    # Confirmar los cambios en la base de datos
    db.session.commit()
    
    return user

def delete_user(user_id):
    db.session.query(User).filter(User.id==user_id).delete()
    db.session.commit()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()  # Usa el modelo para buscar el usuario

def login_user(email, password):
    user = get_user_by_email(email)
    if user and bcrypt.check_password_hash(user.password, password):
        return user  # Retorna el usuario si las credenciales son correctas
    return None  # Retorna None si las credenciales son incorrectas

def block_user(user_id):
    user = get_user(user_id)
    if user and user.role_id != 5:  # 5 es el ID del rol System Admin
        user.enabled = False
        db.session.commit()
        return True
    return False

def unblock_user(user_id):
    user = get_user(user_id)
    if user:
        user.enabled = True
        db.session.commit()
        print("DESBLOQUEADO")
        return True
    return False