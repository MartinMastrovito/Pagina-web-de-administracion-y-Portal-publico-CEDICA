from flask import Blueprint, request, jsonify
from src.web.schemas.articles import articles_schema, article_schema
from src.core import publicacion
bp = Blueprint("articles_api", __name__, url_prefix="/api/articles")

@bp.get("/")
def index():
    page = request.args.get('page')
    per_page = request.args.get('per_page')
    id = request.args.get('id')
    if id:
        id = int(id)
        pub = publicacion.get_publicacion(id)
        data = article_schema.dump(pub)
        return data,200
    if page:
        page = int(page)
    if per_page:
        per_page = int(per_page)
    publicaciones = publicacion.obtener_publicaciones(page, per_page)
    data = articles_schema.dump(publicaciones)
    return data,200