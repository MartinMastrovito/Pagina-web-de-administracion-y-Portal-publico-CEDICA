from core import db
from sqlalchemy.dialects.postgresql import JSON

class JYA(db.Model):
    __tablename__ = 'JYA'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Datos personales
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    edad = db.Column(db.Integer)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    
    debts = db.Column(db.Boolean,default=False)
    # Lugar de nacimiento (localidad, provincia)
    lugar_nacimiento = db.Column(JSON, nullable=False)
    
    # Domicilio actual (calle, número, departamento, localidad, provincia)
    domicilio_actual = db.Column(JSON, nullable=False)
    
    # Teléfono actual
    telefono_actual = db.Column(db.String(20))
    
    # Contacto de emergencia (nombre y teléfono)
    contacto_emergencia = db.Column(JSON, nullable=False)
    
    # Becado (sí/no) y porcentaje de beca
    becado = db.Column(db.Boolean, default=False)
    porcentaje_beca = db.Column(db.Float, default=0.0)
    
    # Profesionales que lo atienden (campo libre)
    profesionales_atendiendo = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Persona {self.nombre} {self.apellido}>'

# Ejemplo de un diccionario que podrías almacenar en los campos JSON:
# lugar_nacimiento = {'localidad': 'Ciudad X', 'provincia': 'Provincia Y'}
# domicilio_actual = {'calle': 'Calle Z', 'numero': 123, 'departamento': 'A', 'localidad': 'Ciudad X', 'provincia': 'Provincia Y'}
# contacto_emergencia = {'nombre': 'Juan Pérez', 'telefono': '123456789'}