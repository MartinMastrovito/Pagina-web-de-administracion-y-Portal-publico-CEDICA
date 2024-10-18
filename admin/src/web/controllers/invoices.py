"""
Esto es un controlador relacionado con los cobros de los J&A. 
"""
from flask import render_template, request, Blueprint, redirect, flash
from src.core.invoices.invoices import Invoices
from core import db
from core.invoices import utiles 




invoices_bp = Blueprint("invoices", __name__,url_prefix="/cobros", template_folder='../templates/invoices',static_folder="/admin/static")

#Ruta del menu principal
@invoices_bp.route("/")
def invoices_menu():
    return render_template("invoices_menu.html",invoices=invoices_bp)

#Rutas del listado de cobros
@invoices_bp.get("/lista-cobros/<int:page>")
def invoices_index(page):
    invoices = db.paginate(db.select(Invoices),page=page,max_per_page=10)
    return render_template("list_invoices.html", invoices=invoices,eliminado=True)

@invoices_bp.post("/lista-cobros/")
def delete_invoice():
    id_delete = request.form['id']
    utiles.delete(id_delete)
    return redirect("/cobros/")

#Ruta para actualizar cobro
@invoices_bp.get("/actualizar-cobro/<int:invoice_id>")
def update_invoice(invoice_id):
    invoice = utiles.get_invoice(invoice_id)
    return render_template("update_invoice.html",invoice=invoice)

@invoices_bp.post("/actualizar-cobro/<int:invoice_id>")
def invoice_update(invoice_id):
    invoice_information = {
        "pay_date":request.form['pay_date'],
        "amount":float(request.form['amount']),
        "observations":request.form['observations'],
        "payment_method":request.form['payment_method']
    }
    utiles.update_invoice(invoice_id, **invoice_information)
    return redirect("/cobros/lista-cobros")

#Rutas del creador de cobros
@invoices_bp.get("/crear-cobro")
def invoice_create():
    ja_dictionary = utiles.get_ja()
    return render_template("create_invoice.html",invoices=invoices_bp,jinetes_amazonas=ja_dictionary)

@invoices_bp.post("/crear-cobro")
def create_invoice():                
    invoice_information = {
        "pay_date": request.form['pay_date'],
        "amount": float(request.form['amount']),
        "payment_method": request.form['payment_method'],
        "j_a": request.form['j&a'],
        "recipient": request.form['recipient'],
        "observations": request.form['observations'],
    }
    if(utiles.validate(**invoice_information)):
         utiles.create(**invoice_information)
    else: 
        return redirect('/cobros')
    return redirect('/cobros/crear-cobro')

#ruta para el listado de los estados de deuda
@invoices_bp.get("/deudores")
def invoice_statuses():
    statuses = [1,2,3,4,5]
    return render_template("statuses_list.html",statuses=statuses)