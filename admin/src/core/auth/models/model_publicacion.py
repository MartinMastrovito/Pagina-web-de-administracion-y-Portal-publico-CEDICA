from src.core.database import db
from datetime import datetime, timezone

class Publicacion(db.Model):
    __tablename__ = "publicaciones"

    id = db.Column(db.Integer, primary_key=True)
    fecha_publicacion = db.Column(db.Date, nullable=True)
    fecha_creacion = db.Column(db.Date, default=datetime.now(timezone.utc), nullable=False)
    fecha_actualizacion = db.Column(db.Date, onupdate=datetime.now(timezone.utc), nullable=True)
    titulo = db.Column(db.String(25), nullable=False)
    copete = db.Column(db.String(255), nullable=True)
    contenido = db.Column(db.Text, nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey("empleados.id"), nullable=True)
    estado = db.Column(db.Enum("Borrador", "Publicado", "Archivado", name="estado_publicacion"), default="Borrador")
    nombre_autor = db.Column(db.String(80), nullable=True)

    autor = db.relationship("Empleados", backref=db.backref("publicaciones", lazy=True))

    def __repr__(self):
        return f"<Publicacion {self.titulo}>"