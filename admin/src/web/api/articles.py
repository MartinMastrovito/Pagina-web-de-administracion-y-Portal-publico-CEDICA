from flask import Blueprint
from src.web.schemas.articles import articles_schema
from src.core.invoices import utiles
bp = Blueprint("articles_api", __name__, url_prefix="/api/articles")

@bp.get("/")
def index():
    """Lo estoy probando con cobros porque no tengo el modelo"""
    invoices = utiles.get_all_list()
    data = articles_schema.dump(invoices)
    return {"status":data},200