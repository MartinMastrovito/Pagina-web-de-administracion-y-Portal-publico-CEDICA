from flask import render_template, request, Blueprint
from src.core.invoices.invoices import Invoices 
from core.database import db

"""
Esto es un controlador relacionado con los cobros de los J&A. 
"""


invoices_bp = Blueprint("invoices", __name__,url_prefix="/cobros", template_folder='../templates/invoices')

@invoices_bp.route("/")
def invoices_menu():
    return render_template("invoices_menu.html",invoices=invoices_bp)

@invoices_bp.route("/listado")
def invoices_index():
    invoices = Invoices.query.all()
    return render_template("list_invoices.html", invoices=invoices)
