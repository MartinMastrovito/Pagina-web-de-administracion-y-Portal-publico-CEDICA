from core.auth import utiles

def check_permission(user, permission):
    
    if user is None:
        return False

    # Obtenemos los permisos desde la base de datos
    permissions = utiles.get_permissions(user)
    print(f"Permisos del usuario: {permissions}")

    # Verificamos si el permiso solicitado está en la lista de permisos del usuario
    return permission in permissions