from core import db
from sqlalchemy.dialects.postgresql import JSON

class Document(db.Model):
    __tablename__ = 'document'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jya_dni = db.Column(db.String(20), db.ForeignKey('JYA.dni'), nullable=False)
    nombre_documento = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    jya = db.relationship('JYA', back_populates='documentos')

class Link(db.Model):
    __tablename__ = 'Link'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jya_dni = db.Column(db.String(20), db.ForeignKey('JYA.dni'), nullable=False)
    nombre_enlace = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    jya = db.relationship('JYA', back_populates='documentos')

class JYA(db.Model):
    __tablename__ = 'JYA'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Datos personales
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    edad = db.Column(db.Integer)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    
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
    
    # Relación con documentos
    documentos = db.relationship('Document', back_populates='jya')

    def __repr__(self):
        return f'<Persona {self.nombre} {self.apellido}>'
