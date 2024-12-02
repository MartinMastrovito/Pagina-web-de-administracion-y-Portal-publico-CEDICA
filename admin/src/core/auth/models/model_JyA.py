from src.core.database import db
from sqlalchemy.dialects.postgresql import JSON

class JYA(db.Model):
    __tablename__ = 'JYA'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    debts = db.Column(db.Boolean,default=False)
    lugar_nacimiento = db.Column(JSON, nullable=False)
    domicilio_actual = db.Column(JSON, nullable=False)
    telefono_actual = db.Column(db.String(20), nullable=False)
    contacto_emergencia = db.Column(JSON, nullable=False)
    becado = db.Column(db.Boolean, default=False, nullable=False)
    observaciones_beca = db.Column(db.Text, nullable=True)
    profesionales_atendiendo = db.Column(db.Text, nullable=True)
    certificado_discapacidad = db.Column(db.Boolean, default=False, nullable=False)
    diagnostico_discapacidad = db.Column(db.String, nullable=True)
    tipo_discapacidad = db.Column(db.Enum('Mental', 'Motora', 'Sensorial', 'Visceral', name='tipo_discapacidad'), nullable=True)
    asignacion_familiar = db.Column(db.Boolean, default=False, nullable=False)
    tipo_asignacion = db.Column(db.String, nullable=True)
    pension = db.Column(db.Boolean, default=False, nullable=False)
    tipo_pension = db.Column(db.String, nullable=True)
    obra_social = db.Column(db.String, nullable=True)
    numero_afiliado = db.Column(db.String, nullable=True)
    curatela = db.Column(db.Boolean, default=False, nullable=False)
    observaciones_previsionales = db.Column(db.Text, nullable=True)
    institucion_escolar = db.Column(JSON, nullable=False)
    familiares_tutores = db.Column(JSON, nullable=True)
    propuesta_trabajo = db.Column(db.String, nullable=False)
    condicion_trabajo = db.Column(db.Enum('REGULAR', 'DE BAJA', name='condicion_trabajo'), nullable=False)
    sede = db.Column(db.String, nullable=False)
    dias_asistencia = db.Column(JSON, nullable=False)
    empleados = db.relationship('JYAEmpleado', back_populates='jya', cascade="all, delete-orphan")
    caballo_id = db.Column(db.Integer, db.ForeignKey('caballos.id'), nullable=True)
    caballo = db.relationship('Caballo', back_populates='jyas')
    documentos = db.relationship('Documento', backref='jya', lazy=True)

    eliminado = db.Column(db.Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f'<Persona {self.nombre} {self.apellido}>'