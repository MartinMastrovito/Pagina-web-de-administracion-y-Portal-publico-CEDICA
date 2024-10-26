from src.core.auth import utiles



def check_permission(session, permission):
    user_email = session.get("user")
    user = utiles.get_user_by_email(user_email)

    if user is None:
        return False

    # Obtenemos los permisos desde la base de datos
    permissions = utiles.get_permissions(user.id)
    print(f"Permisos del usuario: {permissions}")

    # Verificamos si el permiso solicitado está en la lista de permisos del usuario
    return permission in permissions

def check_authenticated(session):
    return session.get("user") is not None