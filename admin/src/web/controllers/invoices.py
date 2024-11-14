"""
Esto es un controlador relacionado con los cobros de los J&A. 
"""
from flask import render_template, request, Blueprint, redirect, flash
from src.core.invoices.invoices import Invoices
from src.core.database import db
from src.core.invoices import utiles
from src.core.auth.decorators import login_required, check




invoices_bp = Blueprint("invoices", __name__,url_prefix="/cobros", template_folder='../templates/invoices',static_folder="/admin/static")

#Ruta del menu principal
@invoices_bp.route("/")
#@login_required
#@check("invoice_menu")
def invoices_menu():
    return render_template("invoices_menu.html",invoices=invoices_bp)

#Rutas del listado de cobros
@invoices_bp.get("/lista-cobros/<int:page>")
#@login_required
#@check("invoice_index")
def invoices_index(page,**order):
    if(len(order) != 0):
        invoices = utiles.select_filter(**order)
    else:
        invoices = utiles.select_all()
    ja_dictionary = utiles.get_all_ja()
    emp_dictionary = utiles.get_all_employees()
    invoices = db.paginate(invoices,page=page,max_per_page=10)
    return render_template("list_invoices.html", invoices=invoices,jinetes_amazonas = ja_dictionary, employees=emp_dictionary)


@invoices_bp.post("/lista-cobros/")
#@login_required
#@check("invoice_index")
def order_list():
    if("id" in request.form):
        return delete_invoice()
    else:
        order_information = {
            "payment_method" : request.form['payment_method'],
            "date_from": request.form['from'],
            "date_to": request.form['to'],
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "order": request.form['order']
        }
        return invoices_index(1,**order_information)

@invoices_bp.post("/lista-cobros/")
#@login_required
#@check("invoice_destroy")
def delete_invoice():
    id_delete = request.form['id']
    utiles.delete(id_delete)
    return redirect("/cobros/")


#Ruta para actualizar cobro
@invoices_bp.get("/actualizar-cobro/<int:invoice_id>")
#@login_required
#@check("invoice_update")
def update_invoice(invoice_id):
    invoice = utiles.get_invoice(invoice_id)
    return render_template("update_invoice.html",invoice=invoice)

@invoices_bp.post("/actualizar-cobro/<int:invoice_id>")
#@login_required
#@check("invoice_update")
def invoice_update(invoice_id):
    invoice_information = {
        "pay_date":request.form['pay_date'],
        "amount":(request.form['amount']),
        "observations":request.form['observations'],
        "payment_method":request.form['payment_method']
    }
    utiles.update_invoice(invoice_id, **invoice_information)
    return redirect("/cobros/lista-cobros/1")

#Rutas del creador de cobros
@invoices_bp.get("/crear-cobro")
#@login_required
#@check("invoice_create")
def invoice_create():
    ja_dictionary = utiles.get_all_ja()
    emp_dictionary = utiles.get_all_employees()
    return render_template("create_invoice.html",invoices=invoices_bp,jinetes_amazonas=ja_dictionary,employees = emp_dictionary)

@invoices_bp.post("/crear-cobro")
#@login_required
#@check("invoice_create")
def create_invoice():                
    invoice_information = {
        "pay_date": request.form['pay_date'],
        "amount": float(request.form['amount']),
        "payment_method": request.form['payment_method'],
        "j_a": request.form['j&a'],
        "recipient": request.form['recipient'],
        "observations": request.form['observations'],
    }
    if(utiles.validate_create(**invoice_information)):
         utiles.create(**invoice_information)
    else: 
        return redirect('/cobros')
    return redirect('/cobros/crear-cobro')

#rutas para el listado de los estados de deuda
@invoices_bp.get("/deudores")
#@login_required
#@check("invoice_index")
def invoice_statuses():
    ja_dictionary = utiles.get_all_ja()
    statuses_dictionary = utiles.get_statuses()
    return render_template("statuses_list.html",invoices=invoices_bp,jinetes_amazonas=ja_dictionary, statuses = statuses_dictionary)

@invoices_bp.post("/deudores")
#@login_required
#@check("invoice_update")
def update_status():
    ja_update = request.form['id']
    utiles.change_status(ja_update)
    return redirect('/cobros/deudores')

#rutas para la muestra de un cobro especifico.
@invoices_bp.get("/mostrar-cobro/<int:invoice_id>")
#@login_required
#@check("invoice_show")
def show_invoice(invoice_id):
    invoice = utiles.get_invoice(invoice_id)
    ja_name = utiles.get_ja(invoice.j_a)
    emp_name = utiles.get_emp(invoice.recipient)
    return render_template("show_invoice.html",invoice=invoice, ja_name= ja_name, emp_name = emp_name)
