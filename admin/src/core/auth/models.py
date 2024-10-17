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
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    
class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    __table_args__ = {'extend_existing': True}
    role_id = db.Column(db.BigInteger, db.ForeignKey('role.id'), primary_key=True)
    permission_id = db.Column(db.BigInteger, db.ForeignKey('permissions.id'), primary_key=True)
    
class Empleados(db.Model):
    __tablename__ = "Empleados"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, index=True)
    nombre = db.Column(db.String, index=True)
    apellido = db.Column(db.String, index=True)
    dni = db.Column(db.String, unique=True, index=True)
    domicilio = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    localidad = db.Column(db.String)
    telefono = db.Column(db.String)
    profesion = db.Column(db.String)
    puesto = db.Column(db.String)
    fecha_inicio = db.Column(db.Date)
    fecha_cese = db.Column(db.Date, nullable=True)
    contacto_emergencia = db.Column(db.String)
    obra_social = db.Column(db.String, nullable=True)
    numero_afiliado = db.Column(db.String, nullable=True)
    condicion = db.Column(db.String)
    activo = db.Column(db.Boolean, default=True)


class Pago(db.Model):
    __tablename__ = 'Pago'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    beneficiario_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=True) # empleado dado de alta en el sistema si es pago de honorarios, si aplica
    monto = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.Date)
    tipo_pago = db.Column(db.String, nullable=False)  #puede ser tipo: honorarios, proveedor o gastos varios
    description = db.Column(db.String, nullable=True)
    
    beneficiary = db.relationship("Empleados", backref="Pagos")


