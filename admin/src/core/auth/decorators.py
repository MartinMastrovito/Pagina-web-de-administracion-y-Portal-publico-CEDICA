from functools import wraps
from flask import session, redirect, url_for, flash
from web.handlers.auth import check_permission

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  # Verificamos si hay una sesión activa, esperemos que no rompa todo
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('users.show_login_form'))
        return f(*args, **kwargs)
    return decorated_function

def check(permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = session.get("user_id")
            print(f"Email del usuario: {user_id}")
            if not check_permission(user_id, permission):
                print(f"Permiso {permission} no encontrado para el usuario.")
                return redirect(url_for("users.show_home"))
            
            print(f"Permiso {permission} encontrado para el usuario.")
            return f(*args, **kwargs)
        
        return wrapper
    
    return decorator
