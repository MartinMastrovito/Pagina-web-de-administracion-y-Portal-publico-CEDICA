from src.core.database import db
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
    observaciones_beca = db.Column(db.Text, nullable=True)
    # Profesionales que lo atienden (campo libre)
    profesionales_atendiendo = db.Column(db.Text, nullable=True)
    
    # Discapacidad
    certificado_discapacidad = db.Column(db.Boolean, default=False)
    diagnostico_discapacidad = db.Column(db.String, nullable=True)
    tipo_discapacidad = db.Column(db.Enum('Mental', 'Motora', 'Sensorial', 'Visceral', name='tipo_discapacidad'), nullable=True)

    # Asignaciones familiares
    asignacion_familiar = db.Column(db.Boolean, default=False)
    tipo_asignacion = db.Column(db.String, nullable=True)
    
    # Pensión
    pension = db.Column(db.Boolean, default=False)
    tipo_pension = db.Column(db.String, nullable=True)

    # Situación previsional
    obra_social = db.Column(db.String, nullable=True)
    numero_afiliado = db.Column(db.String, nullable=True)
    curatela = db.Column(db.Boolean, default=False)
    observaciones_previsionales = db.Column(db.Text, nullable=True)
    
    # Institución escolar
    institucion_escolar = db.Column(JSON, nullable=True)
    
    # Familiares o tutores responsables
    familiares_tutores = db.Column(JSON, nullable=True)
    
    # Actividad en la institución
    propuesta_trabajo = db.Column(db.String, nullable=True)
    condicion_trabajo = db.Column(db.Enum('REGULAR', 'DE BAJA', name='condicion_trabajo'), nullable=True)
    sede = db.Column(db.String, nullable=True)
    dias_asistencia = db.Column(JSON, nullable=True)

    # Relación con empleados (a través de la tabla intermedia JYAEmpleado)
    empleados = db.relationship('JYAEmpleado', back_populates='jya')
    
    caballos = db.relationship('Caballo', secondary='caballo_tipoja', back_populates='JYA')
    documentos = db.relationship('Documento', backref='jya', lazy=True)

    def __repr__(self):
        return f'<Persona {self.nombre} {self.apellido}>'