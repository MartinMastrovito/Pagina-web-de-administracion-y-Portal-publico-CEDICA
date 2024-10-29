from src.core.auth.models.model_user import Role
from src.core.auth.models.model_permission import Permission
from src.core.database import db

def role_create():
    """
        Carga los roles en la base de datos
    """
    
    #Roles del sistema
    tecnica = Role(
        id = 1,
        name = "tecnica"
    )
    ecuestre = Role(
        id = 2,
        name = "ecuestre"
    )
    voluntariado = Role(
        id = 3,
        name = "voluntariado"
    )
    administracion = Role(
        id =4,
        name = "administracion" 
    )
    sysadmin = Role(
        id = 5,
        name ="sysadmin" 
    )

    db.session.add(tecnica)
    db.session.add(ecuestre)
    db.session.add(voluntariado)
    db.session.add(administracion)
    db.session.add(sysadmin)
    db.session.commit()


def permission_create():
    # Creación de las instancias de permisos con sus respectivos nombres
    user_index = Permission(name="user_index")
    user_new = Permission(name="user_new")
    user_destroy = Permission(name="user_destroy")
    user_show = Permission(name="user_show")
    jya_index = Permission(name="jya_index")
    jya_new = Permission(name="jya_new")
    jya_destroy = Permission(name="jya_destroy")
    jya_update = Permission(name="jya_update")
    jya_show = Permission(name="jya_show")
    db.session.add(user_index)
    db.session.add(user_new)
    db.session.add(user_destroy)
    db.session.add(user_show)
    db.session.add(jya_index)
    db.session.add(jya_new)
    db.session.add(jya_destroy)
    db.session.add(jya_update)
    db.session.add(jya_show)
    db.session.commit()

def db_seeds():
    role_create()
    permission_create()