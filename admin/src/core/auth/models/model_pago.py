from src.core.database import db

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

