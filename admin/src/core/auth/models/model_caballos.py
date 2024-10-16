from core import db
from core.auth.models.model_documento import Documento
from core.auth.models.model_JyA import TipoJA 
from core.auth.models.model_tablasIntermedias import caballo_tipoja , caballo_entrenadores , caballo_conductores


class MiembroEquipo(db.Model):
    __tablename__ = 'miembros_equipo'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)

    entrenados = db.relationship('Caballo', secondary='caballo_entrenadores', back_populates='entrenadores')
    conducidos = db.relationship('Caballo', secondary='caballo_conductores', back_populates='conductores')

    def __repr__(self):
        return f'<MiembroEquipo {self.nombre}>'

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




