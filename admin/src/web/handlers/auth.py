from src.core.auth import utiles



def check_permission(session, permission):

    user = utiles.get_user(session)

    if user is None:
        return False

    permissions = utiles.get_permissions(user.id)

    return permission in permissions

def check_authenticated(session):
    return session.get("user_id") is not None