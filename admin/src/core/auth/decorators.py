from functools import wraps
from flask import session, redirect, url_for, flash
from src.web.handlers.auth import check_permission
from src.core.auth.utiles import get_user_by_email

def login_required(f):
    """
    Decorador que verifica si un usuario se encuentra autenticado.

    Returns:
        function: La función decorada que realiza la verificación de la autenticación.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session and 'profile' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('users.show_login_form'))
        return f(*args, **kwargs)
    return decorated_function


def check(permission):
    """
    Decorador que verifica si un usuario tiene un permiso específico para acceder a una vista.

    Args:
        permission (str): El nombre del permiso que se desea verificar.

    Returns:
        function: La función decorada que realiza la verificación de permisos.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = session.get("user_id")
            user_google = session.get('profile')
            if user_id:
                if not check_permission(session, permission):
                    return redirect(url_for("users.show_home"))
            elif user_google:
                user_email = user_google["email"]
                user = get_user_by_email(user_email)
                if not check_permission(user.id, permission):
                    return redirect(url_for("users.show_home"))
            return f(*args, **kwargs)
        
        return wrapper
    
    return decorator
