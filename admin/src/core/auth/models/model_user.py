from src.core.database import db

class Role(db.Model):
    __tablename__ = 'role'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    permissions = db.relationship('Permission', secondary='role_permissions', backref='roles')
    
    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    alias = db.Column(db.String(50))
    enabled = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  
    role = db.relationship('Role', backref='users')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    eliminado = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'
