from src.core.database import db

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
