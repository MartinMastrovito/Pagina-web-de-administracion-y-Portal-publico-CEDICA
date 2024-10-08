from core.auth.users import Users
from core.bcrypt import bcrypt
from core.database import db
from core.auth.models import User  


def list_users():
    users = Users.query.all()

    return users

def create_user(**kwargs):
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs["password"] = hash.decode("utf-8")
    user = Users(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def get_user(user_id):
    return Users.query.get_or_404(user_id)

def update_user(user_id, **kwargs):
    user = get_user(user_id)
    
    # Actualizar los atributos del usuario con los valores proporcionados en kwargs
    for key, value in kwargs.items():
        setattr(user, key, value)
    
    # Confirmar los cambios en la base de datos
    db.session.commit()
    
    return user

def delete_user(user_id):
    db.session.query(Users).filter(Users.id==user_id).delete()
    db.session.commit()







def get_user_by_email(email):
    return User.query.filter_by(email=email).first()  # Usa el modelo para buscar el usuario
