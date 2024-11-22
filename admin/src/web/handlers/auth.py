from src.core.auth import utiles

def check_permission(session, permission):
    """
    Verifica si el usuario autenticado tiene un permiso específico.

    Args:
        session : Objeto de sesión que contiene información del usuario autenticado.
        permission : El permiso que se desea verificar.

    Returns:
        bool: True si el usuario tiene el permiso, False en caso contrario.
    """
    user_id = session.get("user_id")
    if user_id is None:
        return False
    
    user = utiles.get_user(user_id)
    if user is None:
        return False
    permissions = utiles.get_permissions(user.id)
    
    return permission in permissions

def check_authenticated(session):
    """
    Verifica si hay un usuario autenticado en la sesión actual.

    Args:
        session : Objeto de sesión que contiene información del usuario autenticado.

    Returns:
        bool: True si el usuario está autenticado, False en caso contrario.
    """
    return session.get("user_id") is not None