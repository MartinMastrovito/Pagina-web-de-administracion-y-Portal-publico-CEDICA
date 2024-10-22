from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def init_app(app):
    """Inicializa bcrypt con la aplicación Flask"""
    bcrypt.init_app(app)    

def generate_password_hash(password):
    """Genera el hash de la contraseña"""
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password_hash(hashed_password, password):
    """Verifica si la contraseña coincide con el hash almacenado"""
    return bcrypt.check_password_hash(hashed_password, password)
