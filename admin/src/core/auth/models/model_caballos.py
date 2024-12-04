from src.core.database import db
#from core.auth.models.model_documento import Documento


caballo_entrenadores = db.Table('caballo_entrenadores', 
    db.Column('caballo_id', db.Integer, db.ForeignKey('caballos.id', ondelete='CASCADE'), primary_key=True),
    db.Column('empleado_id', db.Integer, db.ForeignKey('empleados.id', ondelete='CASCADE'), primary_key=True),
    extend_existing=True
)

caballo_conductores = db.Table('caballo_conductores',
    db.Column('caballo_id', db.Integer, db.ForeignKey('caballos.id', ondelete='CASCADE'), primary_key=True),
    db.Column('empleado_id', db.Integer, db.ForeignKey('empleados.id', ondelete='CASCADE'), primary_key=True),
    extend_existing=True
)

caballo_tipoja = db.Table('caballo_tipoja',
    db.Column('caballo_id', db.Integer, db.ForeignKey('caballos.id'), primary_key=True),
    db.Column('JYA_id', db.Integer, db.ForeignKey('JYA.id'), primary_key=True),
    extend_existing=True
)


class Caballo(db.Model):
    __tablename__ = 'caballos'
    __table_args__ = {'extend_existing': True}

    entrenadores = db.relationship('Empleados', secondary='caballo_entrenadores')
    conductores = db.relationship('Empleados', secondary='caballo_conductores')

    documentos = db.relationship('Documento', lazy=True)

    jyas = db.relationship('JYA', back_populates='caballo')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(50), nullable=False)
    raza = db.Column(db.String(255), nullable=True)
    pelaje = db.Column(db.String(255), nullable=True)
    tipo_ingreso = db.Column(db.String(50), nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    sede_asignada = db.Column(db.String(255), nullable=False)
    tipo_ja_asignado = db.Column(db.String(255), nullable=True)
    dado_de_baja = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Caballo {self.nombre}>'





