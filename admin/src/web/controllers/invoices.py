from flask import render_template, request, Blueprint, redirect
from src.core.invoices.invoices import Invoices
from core.database import db

"""
Esto es un controlador relacionado con los cobros de los J&A. 
"""


invoices_bp = Blueprint("invoices", __name__,url_prefix="/cobros", template_folder='../templates/invoices',static_folder="/admin/static")
@invoices_bp.route("/")
def invoices_menu():
    return render_template("invoices_menu.html",invoices=invoices_bp)

@invoices_bp.route("/listado")
def invoices_index():
    invoices = Invoices.query.all()
    return render_template("list_invoices.html", invoices=invoices)

@invoices_bp.get("/crear-cobro")
def invoice_create():
    return render_template("create_invoice.html",invoices=invoices_bp)

@invoices_bp.post("/crear-cobro")
def create_user():
    
    invoice_information = {
        "pay_date": request.form['pay_date'],
        "amount": request.form['amount'],
        "payment_method": request.form['payment_method'],
        "j&a": request.form['j&a'],
        "recipient": request.form['recipient'],
        "observations": request.form['observations'],
    }
    
    db.session.add(invoice_information)
    db.session.commit()
    return redirect('/usuarios')