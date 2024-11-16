from flask import Blueprint
from src.web.schemas.articles import articles_schema
from src.core import publicacion
bp = Blueprint("articles_api", __name__, url_prefix="/api/articles")

@bp.get("/")
def index():
    """Lo estoy probando con cobros porque no tengo el modelo"""
    publicaciones = publicacion.obtener_publicaciones(1,5)
    data = articles_schema.dump(publicaciones)
    return data,200