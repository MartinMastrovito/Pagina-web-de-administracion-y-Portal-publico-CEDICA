from src.core.auth.models.model_user import Role
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







def db_seeds():
    role_create()