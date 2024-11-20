from src.core.database import db

class Consulta(db.Model):
    __tablename__ = 'consultas'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nombre_completo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, default=db.func.current_date())
    estado = db.Column(db.String(50), nullable=False, default='pendiente')
    def __repr__(self):
        return f'<Consulta ID {self.id}>'
