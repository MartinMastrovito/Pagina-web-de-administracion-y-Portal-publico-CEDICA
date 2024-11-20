from src.core.auth.models.model_user import Role, User
from src.core.auth.models.model_permission import Permission, RolePermission
from src.core.auth.models.model_empleado import Empleados
from src.core.auth.models.model_JyA import JYA
from src.core.auth.models.model_publicacion import Publicacion
from src.core.database import db
from src.core import bcrypt
from src.core.auth import utiles
from datetime import datetime

def role_create():
    roles = [
        {"name": "tecnica"},
        {"name": "ecuestre"},
        {"name": "voluntariado"},
        {"name": "administracion"},
        {"name": "sysadmin"}
    ]

    for role_data in roles:
        existing_role = Role.query.filter_by(name=role_data["name"]).first()
        if existing_role:
            print(f"Role with name {role_data['name']} already exists. Skipping.")
            continue

        role = Role(name=role_data["name"])
        db.session.add(role)

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
        # permisos consultas
        Permission(name="consulta_index"),
        Permission(name="consulta_new"),
        Permission(name="consulta_destroy"),
        Permission(name="consulta_update"),
        Permission(name="consulta_show"),
        # permisos publicaciones
        Permission(name="publicacion_index"),
        Permission(name="publicacion_new"),
        Permission(name="publicacion_delete"),
        Permission(name="publicacion_update"),
        Permission(name="publicacion_show"),
        # permisos reportes
        Permission(name="reporte_index"),
        Permission(name="show_reporte"),
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
            Permission.name == "consulta_show",
            Permission.name == "consulta_index",
            Permission.name == "consulta_new",
            Permission.name == "consulta_destroy",
            Permission.name == "consulta_update",
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
            email="ecuestre2@test.com",
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
            dni = "43251238",
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
            dni = "43251556",
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
        JYA(
    nombre = "Carlos",
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
        "nombre":"Maria",
        "telefono": "2215969991",
    },
    becado = False,
    profesionales_atendiendo = "Carlos test",
    certificado_discapacidad = True,
    tipo_discapacidad = "Sensorial",
),

        JYA(
    nombre = "Lucía",
    apellido = "González",
    dni = "39123548",
    edad = 29,
    fecha_nacimiento = "1993-08-19",
    lugar_nacimiento = {
        "localidad": "Mar del Plata",
        "provincia": "Buenos Aires",
    },
    domicilio_actual = {
        "calle": 38,
        "numero": 745,
        "localidad": "Mar del Plata",
        "provincia": "Buenos Aires",
    },
    telefono_actual = "2234567890",
    contacto_emergencia = {
        "nombre":"Jorge",
        "telefono": "2234123456",
    },
    becado = True,
    profesionales_atendiendo = "Lucía test",
    certificado_discapacidad = True,
    tipo_discapacidad = "Mental",
),

        JYA(
    nombre = "Juan",
    apellido = "Perez",
    dni = "40325679",
    edad = 34,
    fecha_nacimiento = "1989-03-25",
    lugar_nacimiento = {
        "localidad": "Rosario",
        "provincia": "Santa Fe",
    },
    domicilio_actual = {
        "calle": 12,
        "numero": 123,
        "localidad": "Rosario",
        "provincia": "Santa Fe",
    },
    telefono_actual = "3415987654",
    contacto_emergencia = {
        "nombre":"Ana",
        "telefono": "3415123456",
    },
    becado = False,
    profesionales_atendiendo = "Juan test",
    certificado_discapacidad = False,
),

        JYA(
    nombre = "Valentina",
    apellido = "Lopez",
    dni = "41234569",
    edad = 27,
    fecha_nacimiento = "1996-07-12",
    lugar_nacimiento = {
        "localidad": "Córdoba",
        "provincia": "Córdoba",
    },
    domicilio_actual = {
        "calle": 21,
        "numero": 458,
        "localidad": "Córdoba",
        "provincia": "Córdoba",
    },
    telefono_actual = "3514561234",
    contacto_emergencia = {
        "nombre":"Diego",
        "telefono": "3514891234",
    },
    becado = True,
    profesionales_atendiendo = "Valentina test",
    certificado_discapacidad = True,
    tipo_discapacidad = "Motora"
),

        JYA(
    nombre = "Santiago",
    apellido = "Martinez",
    dni = "40321599",
    edad = 31,
    fecha_nacimiento = "1992-04-10",
    lugar_nacimiento = {
        "localidad": "Mendoza",
        "provincia": "Mendoza",
    },
    domicilio_actual = {
        "calle": 54,
        "numero": 798,
        "localidad": "Mendoza",
        "provincia": "Mendoza",
    },
    telefono_actual = "2614098765",
    contacto_emergencia = {
        "nombre":"Laura",
        "telefono": "2614109876",
    },
    becado = False,
    profesionales_atendiendo = "Santiago test",
    certificado_discapacidad = False,
),

        JYA(
    nombre = "Agustina",
    apellido = "Ramirez",
    dni = "41432567",
    edad = 28,
    fecha_nacimiento = "1995-01-03",
    lugar_nacimiento = {
        "localidad": "San Juan",
        "provincia": "San Juan",
    },
    domicilio_actual = {
        "calle": 23,
        "numero": 678,
        "localidad": "San Juan",
        "provincia": "San Juan",
    },
    telefono_actual = "2645123456",
    contacto_emergencia = {
        "nombre":"Roberto",
        "telefono": "2645125678",
    },
    becado = True,
    profesionales_atendiendo = "Agustina test",
    certificado_discapacidad = True,
    tipo_discapacidad = "Mental"
),

        JYA(
    nombre = "Rodrigo",
    apellido = "Sosa",
    dni = "42345123",
    edad = 36,
    fecha_nacimiento = "1987-02-16",
    lugar_nacimiento = {
        "localidad": "Salta",
        "provincia": "Salta",
    },
    domicilio_actual = {
        "calle": 15,
        "numero": 341,
        "localidad": "Salta",
        "provincia": "Salta",
    },
    telefono_actual = "3875432190",
    contacto_emergencia = {
        "nombre":"Elena",
        "telefono": "3875321098",
    },
    becado = False,
    profesionales_atendiendo = "Rodrigo test",
    certificado_discapacidad = False,
),

    ]
    db.session.add_all(jya_list)
    db.session.commit()

def articles_create():
    articles_list = [
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-10-10", "%Y-%m-%d").date(),
            titulo="Hola, soy noticia",
            copete="Copetin de noticia",
            contenido="Contenido de noticia",
            autor_id=1
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-10-11", "%Y-%m-%d").date(),
            titulo="Avance en IA",
            copete="Investigadores logran un avance significativo en IA.",
            contenido="El avance permite procesar información de manera más eficiente. Impactará salud, educación y transporte.",
            autor_id=2
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-10-12", "%Y-%m-%d").date(),
            titulo="Receta rápida",
            copete="Receta deliciosa y fácil en 20 minutos.",
            contenido="Pasta con salsa cremosa de aguacate ideal para días ocupados.",
            autor_id=3
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-10-13", "%Y-%m-%d").date(),
            titulo="Clima y salud",
            copete="El cambio climático afecta la salud humana.",
            contenido="Aumento de temperaturas y contaminación agravan enfermedades respiratorias y cardiovasculares.",
            autor_id=4
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-10-14", "%Y-%m-%d").date(),
            titulo="Tecnología educativa",
            copete="IA transforma el aprendizaje.",
            contenido="Herramientas digitales personalizan el aprendizaje y facilitan acceso global.",
            autor_id=5
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-10-15", "%Y-%m-%d").date(),
            titulo="Viaje Antártida",
            copete="Científicos estudian cambio climático.",
            contenido="Investigadores analizarán el impacto del derretimiento de glaciares en niveles del mar.",
            autor_id=6
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-11-20", "%Y-%m-%d").date(),
            titulo="Fósil raro",
            copete="Descubrimiento único en Sudamérica.",
            contenido="Hallazgo bien conservado proporciona información valiosa sobre especies extintas.",
            autor_id=4
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-12-01", "%Y-%m-%d").date(),
            titulo="Misión espacial",
            copete="Lanzan satélite para monitorear climas.",
            contenido="Permite monitorear desastres naturales en tiempo real y mejorar preparación.",
            autor_id=5
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-12-15", "%Y-%m-%d").date(),
            titulo="Vacuna rara",
            copete="Desarrollan vacuna innovadora.",
            contenido="Vacuna combate enfermedad rara con resultados prometedores.",
            autor_id=1
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2025-01-10", "%Y-%m-%d").date(),
            titulo="Robots marinos",
            copete="Exploran ecosistemas marinos.",
            contenido="Robots submarinos recopilan datos sobre vida marina desconocida.",
            autor_id=3
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2025-01-20", "%Y-%m-%d").date(),
            titulo="Energía solar",
            copete="Paneles solares rompen récord.",
            contenido="Nuevo nivel de eficiencia podría revolucionar las energías renovables.",
            autor_id=2
        ),
    ]

    db.session.add_all(articles_list)
    db.session.commit()

def db_seeds():
    role_create()
    permission_create()
    user_create()
    rolePermission_create()
    JYA_create()
    employee_create()
    articles_create()

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
