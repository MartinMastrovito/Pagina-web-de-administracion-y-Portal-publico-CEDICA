from src.core.database import db

class Documento(db.Model):
    __tablename__ = 'documentacion'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nombre_documento = db.Column(db.String(255), nullable=False)
    tipo_documento = db.Column(db.String(255), nullable=False)
    archivo_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=True) 

    empleados = db.relationship('Empleados', back_populates='documentos')
    
    def __repr__(self):
        return f'<Documento {self.nombre_documento}>'
