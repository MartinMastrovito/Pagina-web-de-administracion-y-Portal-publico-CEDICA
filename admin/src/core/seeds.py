from src.core.auth.models.model_user import Role, User
from src.core.auth.models.model_permission import Permission, RolePermission
from src.core.auth.models.model_empleado import Empleados
from src.core.auth.models.model_caballos import Caballo
from src.core.auth.models.model_JyA import JYA
from src.core.auth.models.model_pago import Pago
from src.core.auth.models.model_JYAEmpleado import JYAEmpleado
from src.core.auth.models.model_publicacion import Publicacion
from src.core.invoices.invoices import Invoices
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
        {"name": "editor"},
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
        Permission(name="user_accept"),
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
            Permission.name == "invoice_menu",
            Permission.name == "invoice_index",
            Permission.name == "invoice_show",
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
            Permission.name == "publicacion_index",
            Permission.name == "publicacion_new",
            Permission.name == "publicacion_update",
            Permission.name == "publicacion_show",
            Permission.name == "reporte_index",
            Permission.name == "show_reporte",
            
        )
    )
    administration_permissions = []
    for permission in permissions:
        administration_permissions.append(
            RolePermission(role_id=administrator_id, permission_id=permission.id)
        )
    db.session.add_all(administration_permissions)
    db.session.commit()

def editor_rol_create():
    editor_id = Role.query.filter(Role.name == "editor").first().id
    permissions = Permission.query.filter(
        db.or_(
            Permission.name == "publicacion_index",
            Permission.name == "publicacion_new",
            Permission.name == "publicacion_update",
            Permission.name == "publicacion_show",
            
        )
    )
    editor_permissions = []
    for permission in permissions:
        editor_permissions.append(
            RolePermission(role_id=editor_id, permission_id=permission.id)
        )
    db.session.add_all(editor_permissions)
    db.session.commit()

def sysadmin_rol_create():
    permissions = Permission.query.all()
    sysadmin_permissions = []
    for permission in permissions:
        sysadmin_permissions.append(
            RolePermission(role_id=6, permission_id=permission.id)
        )
    db.session.add_all(sysadmin_permissions)
    db.session.commit()

def rolePermission_create():
    sysadmin_rol_create()
    administracion_rol_create()
    ecuestre_rol_create()
    tecnica_rol_create()
    editor_rol_create()

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
            fecha_cese=None,
            contacto_emergencia="+5491134567890",
            obra_social="Medicus",
            numero_afiliado="456789123",
            condicion="Empleado Permanente",
            activo=False,
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
    caballo_1 = Caballo(
        nombre="Pegasus",
        fecha_nacimiento=datetime.strptime("2015-5-12", "%Y-%m-%d").date(),
        sexo="Macho",
        tipo_ingreso="Adopción",
        fecha_ingreso=datetime.strptime("2021-6-1", "%Y-%m-%d").date(),
        sede_asignada="Sede Central",
        pelaje="Blanco",
        raza="Percheron",
        tipo_ja_asignado="Hipoterapia",
    )
    
    caballo_2 = Caballo(
        nombre="Spirit",
        fecha_nacimiento=datetime.strptime("2018-7-20", "%Y-%m-%d").date(),
        sexo="Macho",
        raza="Pura Sangre",
        pelaje="Marrón",
        tipo_ingreso="Donación",
        fecha_ingreso=datetime.strptime("2022-8-15", "%Y-%m-%d").date(),
        sede_asignada="Sede Norte",
        tipo_ja_asignado="Equitación",


    )
    db.session.add_all([caballo_1, caballo_2])
    db.session.commit()

    jya_list = [
        JYA(
            nombre="Carlos",
            apellido="Serebi",
            dni="43251556",
            edad=25,
            fecha_nacimiento=datetime.strptime("1997-12-15", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Berisso", "provincia": "BSAS"},
            domicilio_actual={
                "calle": "Rivadavia",
                "numero": 330,
                "localidad": "Capital",
                "provincia": "BSAS",
            },
            telefono_actual="2215232145",
            contacto_emergencia={"nombre": "Maria", "telefono": "2015032145"},
            becado=False,
            observaciones_beca="Me gustaría tenerla",
            profesionales_atendiendo="Carlos Test",
            certificado_discapacidad=True,
            diagnostico_discapacidad="ECNE",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="OSDE",
            numero_afiliado="129",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Luffy",
            apellido="Monkey D",
            dni="45896301",
            edad=19,
            fecha_nacimiento=datetime.strptime("2005-06-06", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Villa Foosha", "provincia": "East"},
            domicilio_actual={
                "calle": "Arbol",
                "numero": 330,
                "localidad": "Elbaf",
                "provincia": "GrandLine",
            },
            telefono_actual="2213698522",
            contacto_emergencia={"nombre": "Sanji", "telefono": "2210001234"},
            becado=True,
            observaciones_beca="Me sirve para comer",
            profesionales_atendiendo="Chopper",
            certificado_discapacidad=True,
            diagnostico_discapacidad="Escoliosis Leve",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="IOMA",
            numero_afiliado="123",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Margarita",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Mal desempeño académico",
            },
            propuesta_trabajo="Hipoterapia",
            condicion_trabajo="REGULAR",
            sede="HLP",
            dias_asistencia=["Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Nami",
            apellido="Bellmere",
            dni="42345678",
            edad=18,
            fecha_nacimiento=datetime.strptime("2006-01-15", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Cocoyasi", "provincia": "East"},
            domicilio_actual={
                "calle": "Mikan",
                "numero": 25,
                "localidad": "Cocoyasi",
                "provincia": "East",
            },
            telefono_actual="2215678901",
            contacto_emergencia={"nombre": "Nojiko", "telefono": "2214567890"},
            becado=False,
            observaciones_beca="N/A",
            profesionales_atendiendo="Dr. Vegapunk",
            certificado_discapacidad=True,
            diagnostico_discapacidad="Psicosis",
            tipo_discapacidad="Mental",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="IOMA",
            numero_afiliado="289",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Zoro",
            apellido="Roronoa",
            dni="41235678",
            edad=21,
            fecha_nacimiento=datetime.strptime("2002-11-11", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Berisso", "provincia": "BSAS"},
            domicilio_actual={
                "calle": "Espada",
                "numero": 30,
                "localidad": "Shimotsuki",
                "provincia": "BSAS",
            },
            telefono_actual="2215232145",
            contacto_emergencia={"nombre": "Maria", "telefono": "2015032145"},
            becado=False,
            observaciones_beca="Me gustaría tenerla",
            profesionales_atendiendo="Carlos Test",
            certificado_discapacidad=True,
            diagnostico_discapacidad="ECNE",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="OSDE",
            numero_afiliado="123456789",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Florencia",
            apellido="Camargo",
            dni="11444777",
            edad=25,
            fecha_nacimiento=datetime.strptime("1997-12-15", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Berisso", "provincia": "BSAS"},
            domicilio_actual={
                "calle": "Rivadavia",
                "numero": 330,
                "localidad": "Capital",
                "provincia": "BSAS",
            },
            telefono_actual="2215232145",
            contacto_emergencia={"nombre": "Maria", "telefono": "2015032145"},
            becado=True,
            observaciones_beca="Me gusta tenerla",
            profesionales_atendiendo="Carlos DR",
            certificado_discapacidad=True,
            diagnostico_discapacidad="ECNE",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="OSDE",
            numero_afiliado="123456789",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Macarena",
            apellido="Lituan",
            dni="99852258",
            edad=25,
            fecha_nacimiento=datetime.strptime("1997-12-15", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Berisso", "provincia": "BSAS"},
            domicilio_actual={
                "calle": "Rivadavia",
                "numero": 330,
                "localidad": "Capital",
                "provincia": "BSAS",
            },
            telefono_actual="2215232145",
            contacto_emergencia={"nombre": "Maria", "telefono": "2015032145"},
            becado=True,
            observaciones_beca="Me gustaría tenerla",
            profesionales_atendiendo="Carlos Test",
            certificado_discapacidad=True,
            diagnostico_discapacidad="ECNE",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="OSDE",
            numero_afiliado="123456789",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Juan",
            apellido="Figueroa",
            dni="22136136",
            edad=25,
            fecha_nacimiento=datetime.strptime("1997-12-15", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Berisso", "provincia": "BSAS"},
            domicilio_actual={
                "calle": "Rivadavia",
                "numero": 330,
                "localidad": "Capital",
                "provincia": "BSAS",
            },
            telefono_actual="2215232145",
            contacto_emergencia={"nombre": "Maria", "telefono": "2015032145"},
            becado=False,
            observaciones_beca="Me gustaría tenerla",
            profesionales_atendiendo="Carlos Test",
            certificado_discapacidad=True,
            diagnostico_discapacidad="ECNE",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="OSDE",
            numero_afiliado="123456789",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Antonella",
            apellido="Casusa",
            dni="78412256",
            edad=25,
            fecha_nacimiento=datetime.strptime("1997-12-15", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Berisso", "provincia": "BSAS"},
            domicilio_actual={
                "calle": "Rivadavia",
                "numero": 330,
                "localidad": "Capital",
                "provincia": "BSAS",
            },
            telefono_actual="2215232145",
            contacto_emergencia={"nombre": "Maria", "telefono": "2015032145"},
            becado=False,
            observaciones_beca="Me gustaría tenerla",
            profesionales_atendiendo="Carlos Test",
            certificado_discapacidad=True,
            diagnostico_discapacidad="ECNE",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="OSDE",
            numero_afiliado="123456789",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Rodrigo",
            apellido="Bustamante",
            dni="32123321",
            edad=25,
            fecha_nacimiento=datetime.strptime("1997-12-15", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Berisso", "provincia": "BSAS"},
            domicilio_actual={
                "calle": "Rivadavia",
                "numero": 330,
                "localidad": "Capital",
                "provincia": "BSAS",
            },
            telefono_actual="2215232145",
            contacto_emergencia={"nombre": "Maria", "telefono": "2015032145"},
            becado=True,
            observaciones_beca="Me gusta tenerla",
            profesionales_atendiendo="Carlos Test",
            certificado_discapacidad=True,
            diagnostico_discapacidad="ECNE",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="OSDE",
            numero_afiliado="123456789",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Lucio",
            apellido="Folino",
            dni="10100010",
            edad=25,
            fecha_nacimiento=datetime.strptime("1997-12-15", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Berisso", "provincia": "BSAS"},
            domicilio_actual={
                "calle": "Rivadavia",
                "numero": 330,
                "localidad": "Capital",
                "provincia": "BSAS",
            },
            telefono_actual="2215232145",
            contacto_emergencia={"nombre": "Maria", "telefono": "2015032145"},
            becado=False,
            observaciones_beca="Me gustaría tenerla",
            profesionales_atendiendo="Carlos Test",
            certificado_discapacidad=True,
            diagnostico_discapacidad="ECNE",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="OSDE",
            numero_afiliado="123456789",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Carlos",
            apellido="Diz",
            dni="32322323",
            edad=25,
            fecha_nacimiento=datetime.strptime("1997-12-15", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Berisso", "provincia": "BSAS"},
            domicilio_actual={
                "calle": "Rivadavia",
                "numero": 330,
                "localidad": "Capital",
                "provincia": "BSAS",
            },
            telefono_actual="2215232145",
            contacto_emergencia={"nombre": "Maria", "telefono": "2015032145"},
            becado=False,
            observaciones_beca="Me gustaría tenerla",
            profesionales_atendiendo="Carlos Test",
            certificado_discapacidad=True,
            diagnostico_discapacidad="ECNE",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="OSDE",
            numero_afiliado="123456789",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Flavia",
            apellido="Belinche",
            dni="28868240",
            edad=25,
            fecha_nacimiento=datetime.strptime("1997-12-15", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Berisso", "provincia": "BSAS"},
            domicilio_actual={
                "calle": "Rivadavia",
                "numero": 330,
                "localidad": "Capital",
                "provincia": "BSAS",
            },
            telefono_actual="2215232145",
            contacto_emergencia={"nombre": "Maria", "telefono": "2015032145"},
            becado=False,
            observaciones_beca="Me gustaría tenerla",
            profesionales_atendiendo="Carlos Test",
            certificado_discapacidad=True,
            diagnostico_discapacidad="ECNE",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="OSDE",
            numero_afiliado="123456789",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Palta",
            apellido="Verde",
            dni="66321030",
            edad=25,
            fecha_nacimiento=datetime.strptime("1997-12-15", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Berisso", "provincia": "BSAS"},
            domicilio_actual={
                "calle": "Rivadavia",
                "numero": 330,
                "localidad": "Capital",
                "provincia": "BSAS",
            },
            telefono_actual="2215232145",
            contacto_emergencia={"nombre": "Maria", "telefono": "2015032145"},
            becado=False,
            observaciones_beca="Me gustaría tenerla",
            profesionales_atendiendo="Carlos Test",
            certificado_discapacidad=True,
            diagnostico_discapacidad="ECNE",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="OSDE",
            numero_afiliado="123456789",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Julian",
            apellido="Alvarez",
            dni="11222330",
            edad=25,
            fecha_nacimiento=datetime.strptime("1997-12-15", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Berisso", "provincia": "BSAS"},
            domicilio_actual={
                "calle": "Rivadavia",
                "numero": 330,
                "localidad": "Capital",
                "provincia": "BSAS",
            },
            telefono_actual="2215232145",
            contacto_emergencia={"nombre": "Maria", "telefono": "2015032145"},
            becado=True,
            observaciones_beca="Me gusta tenerla",
            profesionales_atendiendo="Carlos Test",
            certificado_discapacidad=True,
            diagnostico_discapacidad="ECNE",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="OSDE",
            numero_afiliado="123456789",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
        JYA(
            nombre="Pablo",
            apellido="Catanzaro",
            dni="74457457",
            edad=25,
            fecha_nacimiento=datetime.strptime("1997-12-15", "%Y-%m-%d").date(),
            lugar_nacimiento={"localidad": "Berisso", "provincia": "BSAS"},
            domicilio_actual={
                "calle": "Rivadavia",
                "numero": 330,
                "localidad": "Capital",
                "provincia": "BSAS",
            },
            telefono_actual="2215232145",
            contacto_emergencia={"nombre": "Maria", "telefono": "2015032145"},
            becado=True,
            observaciones_beca="Me gustaría tenerla",
            profesionales_atendiendo="Carlos Test",
            certificado_discapacidad=True,
            diagnostico_discapacidad="ECNE",
            tipo_discapacidad="Motora",
            asignacion_familiar=True,
            tipo_asignacion="Asignación Universal por hijo",
            pension=True,
            tipo_pension="Provincial",
            obra_social="OSDE",
            numero_afiliado="123456789",
            curatela=False,
            observaciones_previsionales="Observaciones bastante previsionales",
            institucion_escolar={
                "nombre": "Santa Rosa",
                "direccion": "Calle 82, Berisso",
                "telefono": "2211234567",
                "grado_actual": "6to Año",
                "observaciones": "Buen desempeño académico",
            },
            propuesta_trabajo="Deporte",
            condicion_trabajo="REGULAR",
            sede="CASJ",
            dias_asistencia=["Lunes", "Miércoles", "Viernes"],
            caballo_id=caballo_1.id,
        ),
    ]
    
    db.session.add_all(jya_list)
    db.session.commit()

    relaciones_jya_empleado = [
        JYAEmpleado(jya_id=1, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=1, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=1, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=2, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=2, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=2, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=3, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=3, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=3, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=4, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=4, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=4, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=5, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=5, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=5, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=6, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=6, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=6, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=7, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=7, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=7, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=8, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=8, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=8, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=9, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=9, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=9, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=10, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=10, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=10, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=11, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=11, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=11, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=12, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=12, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=12, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=13, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=13, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=13, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=14, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=14, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=14, empleado_id=5, rol="auxiliar"),
        
        JYAEmpleado(jya_id=15, empleado_id=6, rol="terapeuta"),
        JYAEmpleado(jya_id=15, empleado_id=3, rol="conductor"),
        JYAEmpleado(jya_id=15, empleado_id=5, rol="auxiliar"),
    ]

    db.session.add_all(relaciones_jya_empleado)
    db.session.commit()

def articles_create():
    articles_list = [
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            fecha_actualizacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            titulo="Hola, soy noticia",
            copete="Un saludo desde el mundo de las noticias, explorando los eventos más relevantes del día con un enfoque único.",
            contenido="Hoy presentamos una noticia que captura la esencia de los sucesos diarios. Este artículo analiza en profundidad eventos clave, explicando su impacto y relevancia en la sociedad moderna. Descubre cómo pequeños detalles pueden influir en grandes cambios.",
            autor_id=1,
            nombre_autor="China Romero",
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            fecha_actualizacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            titulo="Nuevo avance en IA",
            copete="Investigadores logran un avance significativo en el campo de la inteligencia artificial, transformando el futuro de la tecnología.",
            contenido="Los desarrollos recientes en inteligencia artificial están marcando una nueva era en la computación. Este avance mejora significativamente la eficiencia de los algoritmos, reduciendo los tiempos de respuesta en un 40%. Las aplicaciones potenciales incluyen diagnósticos médicos más rápidos, sistemas educativos personalizados y optimización de procesos industriales. La comunidad científica está entusiasmada con las posibilidades que estos avances representan.",
            autor_id=2,
            nombre_autor="Mulan Ramirez",
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            fecha_actualizacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            titulo="Receta fácil y rápida",
            copete="Una receta deliciosa para preparar en menos de 20 minutos, perfecta para cualquier ocasión.",
            contenido="¿Tienes poco tiempo pero quieres disfrutar de una comida deliciosa? Prueba esta receta de pasta con salsa cremosa de aguacate. Usando ingredientes simples como aguacate fresco, ajo y jugo de limón, puedes crear una cena nutritiva y rápida. Este plato no solo es saludable, sino que también impresiona con su sabor fresco y textura cremosa. Ideal para cenas familiares o momentos de apuro.",
            autor_id=3,
            nombre_autor="Juana Ramirez",
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            fecha_actualizacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            titulo="Clima y salud",
            copete="El cambio climático afecta la salud humana de formas más profundas de lo que imaginamos.",
            contenido="Un estudio reciente revela que el aumento de las temperaturas globales, combinado con la contaminación del aire, está causando un incremento alarmante de enfermedades respiratorias y cardiovasculares. Las poblaciones más vulnerables, incluidas las personas mayores y niños, enfrentan un riesgo elevado. Este artículo analiza las posibles soluciones para mitigar estos efectos, desde políticas más estrictas hasta tecnologías limpias.",
            autor_id=4,
            nombre_autor="Juan Ramirez",
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            fecha_actualizacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            titulo="Tecnología educativa",
            copete="La tecnología está revolucionando la forma en que aprendemos y accedemos al conocimiento.",
            contenido="Con la introducción de herramientas digitales y sistemas de inteligencia artificial en las aulas, el aprendizaje se ha vuelto más interactivo y accesible. Plataformas en línea permiten a los estudiantes de todo el mundo acceder a recursos educativos de alta calidad. Este artículo explora cómo estas innovaciones están democratizando la educación y ayudando a cerrar brechas de conocimiento en regiones desfavorecidas.",
            autor_id=5,
            nombre_autor="Franco Maldini",
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            fecha_actualizacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            titulo="Viaje Antártida",
            copete="Un grupo de científicos se aventura en un viaje épico para investigar los efectos del cambio climático.",
            contenido="Este viaje científico, de seis meses de duración, busca estudiar el impacto del derretimiento de los glaciares en el nivel del mar. Equipos multidisciplinarios analizarán datos clave para comprender cómo estas transformaciones están afectando los ecosistemas globales. Los resultados podrían proporcionar la base para nuevas políticas ambientales y acciones urgentes.",
            autor_id=6,
            nombre_autor="Sofia Ramirez",
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            fecha_actualizacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            titulo="Fósil raro",
            copete="Un descubrimiento sin precedentes arroja luz sobre especies extintas de hace millones de años.",
            contenido="En un yacimiento arqueológico de Sudamérica, investigadores hallaron un fósil excepcionalmente bien conservado que podría cambiar lo que sabemos sobre la evolución de varias especies. Este hallazgo no solo aporta datos paleontológicos, sino que también abre nuevas preguntas sobre los ecosistemas de épocas pasadas.",
            autor_id=4,
            nombre_autor="Linus Tenaglia",
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            fecha_actualizacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            titulo="Misión espacial",
            copete="Se lanza un satélite revolucionario para monitorear el clima en tiempo real.",
            contenido="La agencia espacial internacional ha lanzado un satélite avanzado diseñado para observar desastres naturales y patrones climáticos con una precisión sin precedentes. Los datos recopilados ayudarán a los gobiernos a planificar mejor las respuestas ante emergencias climáticas, salvando vidas y reduciendo daños.",
            autor_id=5,
            nombre_autor="Juan Fin",
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            fecha_actualizacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            titulo="Vacuna rara",
            copete="Un avance médico promete cambiar la vida de miles de personas en todo el mundo.",
            contenido="Científicos han desarrollado una vacuna innovadora para combatir una enfermedad rara que afecta a menos del 1% de la población global. Los ensayos clínicos iniciales han mostrado resultados positivos, y la comunidad médica está entusiasmada con su potencial para reducir los síntomas y mejorar la calidad de vida de los pacientes.",
            autor_id=1,
            nombre_autor="Piscu Lichi",
        ),
        Publicacion(
            fecha_publicacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            fecha_actualizacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            titulo="Robots marinos",
            copete="Exploradores robóticos están transformando la investigación marina.",
            contenido="Ingenieros han presentado robots submarinos equipados con sensores avanzados capaces de recopilar datos en áreas inaccesibles para los humanos. Estas máquinas están revelando secretos ocultos de los océanos, incluyendo ecosistemas inexplorados y patrones de vida marina que podrían ser clave para la conservación.",
            autor_id=3,
            nombre_autor="Juan Roman",
        ),
        Publicacion(
            fecha_actualizacion=datetime.strptime("2024-11-27", "%Y-%m-%d").date(),
            titulo="Energía solar",
            copete="Nueva tecnología en paneles solares promete revolucionar el mercado energético.",
            contenido="Un grupo de investigadores ha desarrollado paneles solares con niveles de eficiencia nunca antes vistos. Este avance podría reducir significativamente los costos de la energía renovable, impulsando una adopción masiva y acelerando la transición hacia un futuro sostenible.",
            autor_id=2,
            nombre_autor="Fabra Ramirez",
        ),
    ]

    db.session.add_all(articles_list)
    db.session.commit()

def invoices_create():
    primer_jya = JYA.query.get(1)
    primer_empleado = Empleados.query.get(1)
    segundo_jya = JYA.query.get(2)
    segundo_empleado = Empleados.query.get(2)
    invoices_list = [
        Invoices(
            ja_first_name = primer_jya.nombre,
            ja_last_name = primer_jya.apellido,
            pay_date = "2024-09-27",
            payment_method = "Efectivo",
            amount = 500,
            recipient_first_name = primer_empleado.nombre,
            recipient_last_name = primer_empleado.apellido,
            observations = "Esto se esta creando desde el seeds :)"
        ),
        Invoices(
            ja_first_name = segundo_jya.nombre,
            ja_last_name = segundo_jya.apellido,
            pay_date = "2024-09-11",
            payment_method = "Tarjeta de credito",
            amount = 76412,
            recipient_first_name = segundo_empleado.nombre,
            recipient_last_name = segundo_empleado.apellido,
            observations = "Esto se esta creando desde el seeds :)"
        )
    ]
    db.session.add_all(invoices_list)
    db.session.commit()

def pagos_create():
    primer_empleado = Empleados.query.get(1)
    segundo_empleado = Empleados.query.get(2)
    pagos_list = [
        Pago(
            beneficiario_id = primer_empleado.id,
            beneficiario_nombre = primer_empleado.nombre,
            beneficiario_apellido = primer_empleado.apellido,
            fecha_pago = "2024-06-07",
            monto = 600,
            tipo_pago = "Honorarios",
            description = "agrego pago",

           
        ),
        Pago(
            beneficiario_id = segundo_empleado.id,
            beneficiario_nombre = segundo_empleado.nombre,
            beneficiario_apellido = segundo_empleado.apellido,
            fecha_pago = "2023-06-07",
            monto = 100,
            tipo_pago = "Honorarios",
            description = "agrego pago 2",

           
        )
    ]
    db.session.add_all(pagos_list)
    db.session.commit()

def db_seeds():
    role_create()
    permission_create()
    user_create()
    rolePermission_create()
    employee_create()
    JYA_create()
    articles_create()
    invoices_create()
    pagos_create()

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
