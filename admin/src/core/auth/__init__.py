from src.core.auth.models.model_user import User
from src.core.bcrypt import bcrypt
from src.core.database import db

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