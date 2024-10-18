from src.core.database import db
from core.auth.models.model_documento import Documento
#from core.auth.models.model_tablasIntermedias import  caballo_entrenadores , caballo_conductores


caballo_entrenadores = db.Table('caballo_entrenadores', 
    db.Column('caballo_id', db.Integer, db.ForeignKey('caballos.id'), primary_key=True),
    db.Column('miembroequipo_id', db.Integer, db.ForeignKey('miembros_equipo.id'), primary_key=True),
    extend_existing=True
)

caballo_conductores = db.Table('caballo_conductores',
    db.Column('caballo_id', db.Integer, db.ForeignKey('caballos.id'), primary_key=True),
    db.Column('miembroequipo_id', db.Integer, db.ForeignKey('miembros_equipo.id'), primary_key=True),
    extend_existing=True
)

class MiembroEquipo(db.Model):
    __tablename__ = 'miembros_equipo'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)

    entrenados = db.relationship('Caballo', secondary='caballo_entrenadores', back_populates='entrenadores')
    conducidos = db.relationship('Caballo', secondary='caballo_conductores', back_populates='conductores')

    def __repr__(self):
        return f'<MiembroEquipo {self.nombre}>'


caballo_tipoja = db.Table('caballo_tipoja',
    db.Column('caballo_id', db.Integer, db.ForeignKey('caballos.id'), primary_key=True),
    db.Column('tipoja_id', db.Integer, db.ForeignKey('tipos_ja.id'), primary_key=True),
    extend_existing=True
)


class Caballo(db.Model):
    __tablename__ = 'caballos'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(50), nullable=False)
    raza = db.Column(db.String(255), nullable=True)
    pelaje = db.Column(db.String(255), nullable=True)
    tipo_ingreso = db.Column(db.String(50), nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    sede_asignada = db.Column(db.String(255), nullable=False)

    entrenadores = db.relationship('MiembroEquipo', secondary='caballo_entrenadores', back_populates='entrenados')
    conductores = db.relationship('MiembroEquipo', secondary='caballo_conductores', back_populates='conductores')

    documentos = db.relationship('Documento', backref='caballo', lazy=True)

    tipos_ja = db.relationship('TipoJA', secondary=caballo_tipoja, back_populates='caballos')

    def __repr__(self):
        return f'<Caballo {self.nombre}>'





