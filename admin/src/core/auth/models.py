#aca se guardan todos los modelos de la base de datos
from datetime import datetime
from core.database import db 

class Role(db.Model):
    __tablename__ = 'role'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)  # Clave primaria para la tabla roles.
    name = db.Column(db.String(50), unique=True, nullable=False)  # Nombre del rol, único y no nulo.

    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    alias = db.Column(db.String(50))
    enabled = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  
    # Definición de la relación entre User y Role.
    role = db.relationship('models.Role', backref='user')


    def __repr__(self):
        return f'<User {self.email}>'





class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    
class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    role_id = db.Column(db.BigInteger, db.ForeignKey('role.id'), primary_key=True)
    permission_id = db.Column(db.BigInteger, db.ForeignKey('permissions.id'), primary_key=True)



from src.core.database import db
from datetime import date

class Caballo(db.Model):
    __tablename__ = 'caballos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(50), nullable=False)
    raza = db.Column(db.String(255), nullable=True)
    pelaje = db.Column(db.String(255), nullable=True)
    tipo_ingreso = db.Column(db.String(50), nullable=False)  # Compra o Donación
    fecha_ingreso = db.Column(db.Date, nullable=False)
    sede_asignada = db.Column(db.String(255), nullable=False)

    # Relación con entrenadores y conductores (miembros del equipo)
    entrenadores = db.relationship('MiembroEquipo', secondary='caballo_entrenadores', back_populates='entrenados')
    conductores = db.relationship('MiembroEquipo', secondary='caballo_conductores', back_populates='conducidos')

    # Relación con tipos de J&A (Hipoterapia, Monta Terapéutica, etc.)
    tipos_ja = db.relationship('TipoJA', secondary='caballo_tipoja', back_populates='caballos')

    # Relación con documentos adjuntos
    documentos = db.relationship('Documento', backref='caballo', lazy=True)

    def __repr__(self):
        return f'<Caballo {self.nombre}>'

# Tabla intermedia para la relación Caballo - Entrenadores
caballo_entrenadores = db.Table('caballo_entrenadores',
    db.Column('caballo_id', db.Integer, db.ForeignKey('caballos.id'), primary_key=True),
    db.Column('miembroequipo_id', db.Integer, db.ForeignKey('miembros_equipo.id'), primary_key=True)
)

# Tabla intermedia para la relación Caballo - Conductores
caballo_conductores = db.Table('caballo_conductores',
    db.Column('caballo_id', db.Integer, db.ForeignKey('caballos.id'), primary_key=True),
    db.Column('miembroequipo_id', db.Integer, db.ForeignKey('miembros_equipo.id'), primary_key=True)
)

# Tabla intermedia para la relación Caballo - Tipos de J&A
caballo_tipoja = db.Table('caballo_tipoja',
    db.Column('caballo_id', db.Integer, db.ForeignKey('caballos.id'), primary_key=True),
    db.Column('tipoja_id', db.Integer, db.ForeignKey('tipos_ja.id'), primary_key=True)
)

class MiembroEquipo(db.Model):
    __tablename__ = 'miembros_equipo'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)

    # Relación inversa con caballos entrenados y conducidos
    entrenados = db.relationship('Caballo', secondary='caballo_entrenadores', back_populates='entrenadores')
    conducidos = db.relationship('Caballo', secondary='caballo_conductores', back_populates='conductores')

    def __repr__(self):
        return f'<MiembroEquipo {self.nombre}>'

class TipoJA(db.Model):
    __tablename__ = 'tipos_ja'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    
    # Relación inversa con caballos
    caballos = db.relationship('Caballo', secondary='caballo_tipoja', back_populates='tipos_ja')

    def __repr__(self):
        return f'<TipoJA {self.nombre}>'

class Documento(db.Model):
    __tablename__ = 'documentos'

    id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    nombre = db.Column(db.String(255), nullable=False)  # Nombre del documento
    tipo_documento = db.Column(db.String(255), nullable=False)  # Tipo de documento (ej: Ficha General, Plan de Entrenamiento, etc.)
    archivo_url = db.Column(db.String(255), nullable=True)  # URL del archivo adjunto o externo

    # Relación con Caballo
    caballo_id = db.Column(db.Integer, db.ForeignKey('caballos.id'), nullable=False)  # Clave foránea que referencia a Caballo

    def __repr__(self):
        return f'<Documento {self.nombre}>'





    
