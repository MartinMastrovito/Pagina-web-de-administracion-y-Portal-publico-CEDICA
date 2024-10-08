

from core.database import db 

class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)  # Clave primaria para la tabla roles.
    name = db.Column(db.String(50), unique=True, nullable=False)  # Nombre del rol, único y no nulo.

    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    alias = db.Column(db.String(50))
    enabled = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  
    # Definición de la relación entre User y Role.
    role = db.relationship('Role', backref='users')

    def __repr__(self):
        return f'<User {self.email}>'
