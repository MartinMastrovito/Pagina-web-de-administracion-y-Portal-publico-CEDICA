from src.core.database import db

beneficiary = db.Table('beneficiary',
    db.Column('pago_id', db.Integer, db.ForeignKey('pago.id'), primary_key=True),
    db.Column('empleados_id', db.Integer, db.ForeignKey('empleados.id'), primary_key=True),
    extend_existing=True
)

class Pago(db.Model):
    __tablename__ = 'pago'  
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    beneficiario_id = db.Column(db.Integer, db.ForeignKey('empleados.id',ondelete='SET NULL'), nullable=True)
    monto = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.Date)
    tipo_pago = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    beneficiario_nombre = db.Column(db.String, nullable=True)
    beneficiario_apellido = db.Column(db.String, nullable=True)    
    
    empleados = db.relationship("Empleados", secondary='beneficiary', back_populates='beneficiary')




