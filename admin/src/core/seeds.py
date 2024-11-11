from src.core.auth.models.model_user import Role, User
from src.core.auth.models.model_permission import Permission, RolePermission
from src.core.auth.models.model_empleado import Empleados
from src.core.auth.models.model_JyA import JYA
from src.core.database import db
from src.core import bcrypt
from src.core.auth import utiles


def role_create():
    """
    Carga los roles en la base de datos
    """

    # Roles del sistema
    list_role = [
        Role(name="tecnica"),
        Role(name="ecuestre"),
        Role(name="voluntariado"),
        Role(name="administracion"),
        Role(name="sysadmin"),
    ]

    db.session.add_all(list_role)
    db.session.commit()


def permission_create():
    # Creación de las instancias de permisos con sus respectivos nombres
    list_permission = [
        # permisos usuarios
        Permission(name="user_index"),
        Permission(name="user_new"),
        Permission(name="user_destroy"),
        Permission(name="user_update"),
        Permission(name="user_show"),
        # permisos jya
        Permission(name="jya_index"),
        Permission(name="jya_new"),
        Permission(name="jya_destroy"),
        Permission(name="jya_update"),
        Permission(name="jya_show"),
        # permisos cobros
        Permission(name="invoice_index"),
        Permission(name="invoice_new"),
        Permission(name="invoice_destroy"),
        Permission(name="invoice_update"),
        Permission(name="invoice_show"),
        Permission(name="invoice_menu"),
        # permisos pagos
        Permission(name="payment_index"),
        Permission(name="payment_new"),
        Permission(name="payment_destroy"),
        Permission(name="payment_update"),
        Permission(name="payment_show"),
        # permisos equipo
        Permission(name="team_index"),
        Permission(name="team_new"),
        Permission(name="team_destroy"),
        Permission(name="team_update"),
        Permission(name="team_show"),
        # permisos caballos
        Permission(name="horse_index"),
        Permission(name="horse_new"),
        Permission(name="horse_destroy"),
        Permission(name="horse_update"),
        Permission(name="horse_show"),
    ]
    db.session.add_all(list_permission)
    db.session.commit()


def tecnica_rol_create():
    tecnica_id = Role.query.filter(Role.name == "tecnica").first().id
    permissions = Permission.query.filter(
        db.or_(
            Permission.name.contains("jya"),
            Permission.name == "horse_index",
            Permission.name == "horse_show",
            Permission.name == "Invoice_menu",
            Permission.name == "Invoice_index",
            Permission.name == "Invoice_show",
        )
    )
    tecnica_permissions = []
    for permission in permissions:
        tecnica_permissions.append(
            RolePermission(role_id=tecnica_id, permission_id=permission.id)
        )
    db.session.add_all(tecnica_permissions)
    db.session.commit()


def ecuestre_rol_create():
    ecuestre_id = Role.query.filter(Role.name == "ecuestre").first().id
    permissions = Permission.query.filter(
        db.or_(
            Permission.name.contains("horse"),
            Permission.name == "jya_index",
            Permission.name == "jya_show",
        )
    )
    ecuestre_permissions = []
    for permission in permissions:
        ecuestre_permissions.append(
            RolePermission(role_id=ecuestre_id, permission_id=permission.id)
        )
    db.session.add_all(ecuestre_permissions)
    db.session.commit()


def administracion_rol_create():
    administrator_id = Role.query.filter(Role.name == "administracion").first().id
    permissions = Permission.query.filter(
        db.or_(
            Permission.name.contains("team"),
            Permission.name.contains("invoice"),
            Permission.name.contains("payment"),
            Permission.name.contains("jya"),
            Permission.name == "horse_index",
            Permission.name == "horse_show",
        )
    )
    administration_permissions = []
    for permission in permissions:
        administration_permissions.append(
            RolePermission(role_id=administrator_id, permission_id=permission.id)
        )
    db.session.add_all(administration_permissions)
    db.session.commit()


def sysadmin_rol_create():
    permissions = Permission.query.all()
    sysadmin_permissions = []
    for permission in permissions:
        sysadmin_permissions.append(
            RolePermission(role_id=5, permission_id=permission.id)
        )
    db.session.add_all(sysadmin_permissions)
    db.session.commit()


def rolePermission_create():
    sysadmin_rol_create()
    administracion_rol_create()
    ecuestre_rol_create()
    tecnica_rol_create()


def user_create():
    list_user = [
        User(
            email="sysadmin@test.com",
            password=bcrypt.generate_password_hash("sysadmin"),
            alias="sysadmin",
            enabled=True,
            role_id=Role.query.filter(Role.name == "sysadmin").first().id,
            created_at="2024-10-29",
        ),
        User(
            email="administracion@test.com",
            password=bcrypt.generate_password_hash("administracion"),
            alias="administracion",
            enabled=True,
            role_id=Role.query.filter(Role.name == "administracion").first().id,
            created_at="2024-10-29",
        ),
        User(
            email="voluntariado@test.com",
            password=bcrypt.generate_password_hash("voluntariado"),
            alias="voluntariado",
            enabled=True,
            role_id=Role.query.filter(Role.name == "voluntariado").first().id,
            created_at="2024-10-29",
        ),
        User(
            email="ecuestre@test.com",
            password=bcrypt.generate_password_hash("ecuestre"),
            alias="ecuestre",
            enabled=True,
            role_id=Role.query.filter(Role.name == "ecuestre").first().id,
            created_at="2024-10-29",
        ),
        User(
            email="tecnica@test.com",
            password=bcrypt.generate_password_hash("tecnica"),
            alias="tecnica",
            enabled=True,
            role_id=Role.query.filter(Role.name == "tecnica").first().id,
            created_at="2024-10-29",
        ),
        User(
            email="bloqueado@test.com",
            password=bcrypt.generate_password_hash("bloqueado"),
            alias="bloqueado",
            enabled=False,
            role_id=Role.query.filter(Role.name == "voluntariado").first().id,
            created_at="2024-10-29",
        ),
        User(
            email="ecuestre@test.com",
            password=bcrypt.generate_password_hash("ecuestre"),
            alias="ecuestre",
            enabled=True,
            role_id=2,
            created_at="2024-10-15",
        ),
    ]
    db.session.add_all(list_user)
    db.session.commit()


def employee_create():
    list_employees = [
        Empleados(
            nombre = "Carlos",
            apellido = "Test",
            dni = "43251231",
            domicilio = "6 1571",
            email = "carlos@test.com",
            localidad = "La Plata",
            telefono = "2215868884",
            profesion = "investigador",
            puesto = "Asistente Administrativo",
            fecha_inicio = "2022-03-15",
            fecha_cese = None,
            contacto_emergencia = "+5491123456789",
            obra_social = "OSDE",
            numero_afiliado = "123456789",
            condicion = "Empleado Permanente",
            activo = True,           
       ),
        Empleados(
            nombre="Laura",
            apellido="González",
            dni="41567890",
            domicilio="25 1025",
            email="laura.gonzalez@example.com",
            localidad="Buenos Aires",
            telefono="1145678910",
            profesion="ingeniera civil",
            puesto="Gerente de Proyectos",
            fecha_inicio="2019-07-01",
            fecha_cese="2023-02-28",
            contacto_emergencia="+5491134567890",
            obra_social="Medicus",
            numero_afiliado="456789123",
            condicion="Empleado Permanente",
            activo=False,
        ),

        Empleados(
            nombre="Martín",
            apellido="Pérez",
            dni="40256789",
            domicilio="12 854",
            email="martin.perez@example.com",
            localidad="Rosario",
            telefono="3414567890",
            profesion="Conductor",
            puesto="Conductor",
            fecha_inicio="2021-06-10",
            fecha_cese=None,
            contacto_emergencia="+5493412345678",
            obra_social="OSDE",
            numero_afiliado="789123456",
            condicion="Empleado Temporal",
            activo=True,
        ),

        Empleados(
            nombre="Ana",
            apellido="López",
            dni="40987654",
            domicilio="8 1923",
            email="ana.lopez@example.com",
            localidad="Mar del Plata",
            telefono="2234567891",
            profesion="Profesor",
            puesto="Profesor",
            fecha_inicio="2020-09-05",
            fecha_cese="2023-09-01",
            contacto_emergencia="+5492234567891",
            obra_social="Swiss Medical",
            numero_afiliado="321654987",
            condicion="Empleado Contratado",
            activo=False,
        ),

        Empleados(
            nombre="José",
            apellido="Martínez",
            dni="38865432",
            domicilio="14 1420",
            email="jose.martinez@example.com",
            localidad="Cordoba",
            telefono="3514567892",
            profesion="Corredor",
            puesto="Auxiliar de pista",
            fecha_inicio="2023-01-10",
            fecha_cese=None,
            contacto_emergencia="+5493514567892",
            obra_social="OSDE",
            numero_afiliado="654987321",
            condicion="Empleado Permanente",
            activo=True,
        ),

        Empleados(
            nombre="Clara",
            apellido="Ramírez",
            dni="41678945",
            domicilio="20 567",
            email="clara.ramirez@example.com",
            localidad="Mendoza",
            telefono="2614567893",
            profesion="Terapeuta",
            puesto="Terapeuta",
            fecha_inicio="2018-04-20",
            fecha_cese="2022-12-15",
            contacto_emergencia="+5492614567893",
            obra_social="Medicus",
            numero_afiliado="112233445",
            condicion="Empleado Contratado",
            activo=False,
        ),
    ]
    db.session.add_all(list_employees)
    db.session.commit()

def JYA_create():
    jya_list = [
        JYA(
            nombre = "carlos",
            apellido = "Serebi",
            dni = "43251551",
            edad = 25,
            fecha_nacimiento = "2022-12-15",
            lugar_nacimiento = {
                "localidad": "La Plata",
                "provincia": "Buenos Aires",
            },
            domicilio_actual = {
                "calle": 6,
                "numero": 330,
                "localidad": "La Plata",
                "provincia": "Buenos Aires",
            },
            telefono_actual = "2215869112",
            contacto_emergencia = {
                "nombre":"maria",
                "telefono": "2215969991",
            },
            becado = False,
            profesionales_atendiendo = "Carlos test",
            certificado_discapacidad = False,
        ),
    ]
    db.session.add_all(jya_list)
    db.session.commit()

def db_seeds():
    role_create()
    permission_create()
    user_create()
    rolePermission_create()
    JYA_create()
    employee_create()

"""
Técnica
    jya_index
    jya_show
    jya_update
    jya_create
    jya_destroy
    caballos_index
    caballos_show
    invoices_menu
    invoices_index
    invoices_show
Ecuestre
    jya_index
    jya_show
    caballos_index
    caballos_show
    caballos_update
    caballos_create
    caballos_destroy
        
Voluntariado:
Administración:
    team_index
    team_show
    team_update
    team_create
    team_destroy
    payment_index
    payment_show
    payment_update
    payment_create
    payment_destroy
    jya_index
    jya_show
    jya_update
    jya_create
    jya_destroy
    caballos_index
    caballos_show
    invoice_index
    invoice_show
    invoice_update
    invoice_new
    invoice_destroy
    invoice_menu
Sysadmin:todo

"""
