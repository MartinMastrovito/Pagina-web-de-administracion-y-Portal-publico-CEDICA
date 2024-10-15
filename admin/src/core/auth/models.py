from datetime import datetime
from core import db 

class Role(db.Model):
    __tablename__ = 'role'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relación con la tabla RolePermission
    permissions = db.relationship('Permission', secondary='role_permissions', backref='roles')
    
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
    role = db.relationship('Role', backref='users')  # Se mantiene la importación directa porque ya está aquí.

    def __repr__(self):
        return f'<User {self.email}>'

class Permission(db.Model):
    __tablename__ = 'permissions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    __table_args__ = {'extend_existing': True}
    role_id = db.Column(db.BigInteger, db.ForeignKey('role.id'), primary_key=True)
    permission_id = db.Column(db.BigInteger, db.ForeignKey('permissions.id'), primary_key=True)

class MiembroEquipo(db.Model):
    __tablename__ = 'miembros_equipo'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)

    entrenados = db.relationship('Caballo', secondary='caballo_entrenadores', back_populates='entrenadores')
    conducidos = db.relationship('Caballo', secondary='caballo_conductores', back_populates='conductores')

    def __repr__(self):
        return f'<MiembroEquipo {self.nombre}>'

class TipoJA(db.Model):
    __tablename__ = 'tipos_ja'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    
    caballos = db.relationship('Caballo', secondary='caballo_tipoja', back_populates='tipos_ja')

    def __repr__(self):
        return f'<TipoJA {self.nombre}>'

class Documento(db.Model):
    __tablename__ = 'documentos'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    tipo_documento = db.Column(db.String(255), nullable=False)
    archivo_url = db.Column(db.String(255), nullable=True)
    caballo_id = db.Column(db.Integer, db.ForeignKey('caballos.id'), nullable=False)

    def __repr__(self):
        return f'<Documento {self.nombre}>'

class Caballo(db.Model):
    __tablename__ = 'caballos'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(50), nullable=False)
    raza = db.Column(db.String(255), nullable=True)
    pelaje = db.Column(db.String(255), nullable=True)
    tipo_ingreso = db.Column(db.String(50), nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    sede_asignada = db.Column(db.String(255), nullable=False)

    entrenadores = db.relationship('MiembroEquipo', secondary='caballo_entrenadores', back_populates='entrenados')
    conductores = db.relationship('MiembroEquipo', secondary='caballo_conductores', back_populates='conductores')

    tipos_ja = db.relationship('TipoJA', secondary='caballo_tipoja', back_populates='caballos')

    documentos = db.relationship('Documento', backref='caballo', lazy=True)

    def __repr__(self):
        return f'<Caballo {self.nombre}>'

# Tablas intermedias
caballo_entrenadores = db.Table('caballo_entrenadores', 
    db.Column('caballo_id', db.Integer, db.ForeignKey('caballos.id'), primary_key=True),
    db.Column('miembroequipo_id', db.Integer, db.ForeignKey('miembros_equipo.id'), primary_key=True),
    extend_existing=True
)

caballo_conductores = db.Table('caballo_conductores',
    db.Column('caballo_id', db.Integer, db.ForeignKey('caballos.id'), primary_key=True),
    db.Column('miembroequipo_id', db.Integer, db.ForeignKey('miembros_equipo.id'), primary_key=True),
    extend_existing=True
)

caballo_tipoja = db.Table('caballo_tipoja',
    db.Column('caballo_id', db.Integer, db.ForeignKey('caballos.id'), primary_key=True),
    db.Column('tipoja_id', db.Integer, db.ForeignKey('tipos_ja.id'), primary_key=True),
    extend_existing=True
)

role = db.relationship('Role', backref='role_permissions')
permission = db.relationship('Permission', backref='role_permissions')