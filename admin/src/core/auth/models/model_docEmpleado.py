from src.core.database import db

class DocumentoEmpleado(db.Model):
    __tablename__ = 'documento_empleado'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nombre_documento = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    empleado_dni= db.Column(db.String, db.ForeignKey('empleados.dni'), nullable=True)
           
    def __repr__(self):
        return f'<Documento {self.nombre}>'
