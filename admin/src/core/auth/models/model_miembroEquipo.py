from src.core.database import db

class MiembroEquipo(db.Model):
    __tablename__ = 'miembros_equipo'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)

    #entrenados = db.relationship('Caballo', secondary='caballo_entrenadores', back_populates='entrenadores')
    #conducidos = db.relationship('Caballo', secondary='caballo_conductores', back_populates='conductores')

    def __repr__(self):
        return f'<MiembroEquipo {self.nombre}>'

