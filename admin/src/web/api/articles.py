from flask import Blueprint, request, jsonify
from src.web.schemas.articles import articles_schema, article_schema
from src.core import publicacion
bp = Blueprint("articles_api", __name__, url_prefix="/api/articles")

@bp.get("/")
def index():
    page = request.args.get('page')
    per_page = request.args.get('per_page')
    id = request.args.get('id')
    titulo = request.args.get('titulo')
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')

    if id:
        id = int(id)
        pub = publicacion.get_publicacion(id)
        data = article_schema.dump(pub)
        retorno = {
            "articles": data
        }
        return retorno,200
    if page:
        page = int(page)
    if per_page:
        per_page = int(per_page)
    filters = {
        'page' : page,
        'per_page' : per_page,
        'titulo' : titulo,
        'desde' : desde,
        'hasta' : hasta
    }
    publicaciones = publicacion.filtrado_portal(**filters)
    pages = publicaciones.pages
    data = articles_schema.dump(publicaciones)
    retorno = {
        "articles": data,
        "pages": pages,
    }
    retorno = jsonify(retorno)
    return retorno,200