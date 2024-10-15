#aca se guardan todos los metodos que se van a usar en la base de datos
#como la comprobacion de login, por ejemplo
from core.bcrypt import bcrypt
<<<<<<< HEAD
from core import db
from core.auth.models import User , Role

=======
from core.database import db
from core.auth.models import User , RolePermission, Permission
>>>>>>> 95f2d408430dabd205217fd9ee0ed3f0e8eea70b

def get_permissions(user):
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

def create_user(**kwargs):
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
