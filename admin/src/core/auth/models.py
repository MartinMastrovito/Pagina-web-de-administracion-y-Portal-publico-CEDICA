#aca se guardan todos los modelos de la base de datos
from datetime import datetime
from core.database import db

class Role(db.Model):
    __tablename__ = 'role'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)  # Clave primaria para la tabla roles.
    name = db.Column(db.String(50), unique=True, nullable=False)  # Nombre del rol, único y no nulo.

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
    
    role = db.relationship('Role', backref='role_permissions')
    permission = db.relationship('Permission', backref='role_permissions')
