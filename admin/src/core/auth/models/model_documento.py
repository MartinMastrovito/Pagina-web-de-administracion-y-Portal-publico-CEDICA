from src.core.database import db

class Documento(db.Model):
    __tablename__ = 'documentos'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nombre_documento = db.Column(db.String(255), nullable=False)
    tipo_documento = db.Column(db.String(255), nullable=False)
    archivo_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    caballo_id = db.Column(db.Integer, db.ForeignKey('caballos.id'), nullable=True)

    jya_dni = db.Column(db.String(20), db.ForeignKey('JYA.dni'), nullable=True)

    def __repr__(self):
        return f'<Documento {self.nombre}>'
