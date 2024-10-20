from src.core.database import db

class Empleados(db.Model):
    __tablename__ = "empleados"
    __table_args__ = {'extend_existing': True}

    beneficiary = db.relationship('Pago', secondary='beneficiary', back_populates='empleados')

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



    def __repr__(self):
        return f'<Empleado {self.nombre},{self.id}>'

