from src.core.database import db

class JYAEmpleado(db.Model):
    __tablename__ = 'jya_empleado'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    jya_id = db.Column(db.Integer, db.ForeignKey('JYA.id'), nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)

    rol = db.Column(db.Enum('profesor', 'terapeuta', 'conductor', 'auxiliar', name='rol_empleado'), nullable=False)
    
    jya = db.relationship('JYA', back_populates='empleados')
    empleado = db.relationship('Empleados', back_populates='jyas_roles')

    def __repr__(self):
        return f'<Asignación {self.jya.nombre} -> {self.empleado.nombre} ({self.rol})>'