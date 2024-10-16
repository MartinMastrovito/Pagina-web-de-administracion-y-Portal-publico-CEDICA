from core import db
from core.auth.models.model_tablasIntermedias import caballo_tipoja , caballo_entrenadores , caballo_conductores

class TipoJA(db.Model):
    __tablename__ = 'tipos_ja'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    
    caballos = db.relationship('Caballo', secondary=caballo_tipoja, back_populates='tipos_ja')

    def __repr__(self):
        return f'<TipoJA {self.nombre}>'
    

