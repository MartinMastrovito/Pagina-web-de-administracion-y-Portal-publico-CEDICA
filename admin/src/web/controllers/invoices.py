"""
Esto es un controlador relacionado con los cobros de los J&A. 
"""
from flask import render_template, request, Blueprint, redirect, flash
from src.core.invoices.invoices import Invoices
from src.core.database import db
from src.core.invoices import utiles
from src.core.auth.decorators import login_required, check
from src.core import crud_JyA




invoices_bp = Blueprint("invoices", __name__,url_prefix="/cobros", template_folder='../templates/invoices',static_folder="/admin/static")

#Ruta del menu principal
@invoices_bp.route("/")
@login_required
@check("invoice_menu")
def invoices_menu():
    return render_template("invoices_menu.html",invoices=invoices_bp)

#Rutas del listado de cobros
@invoices_bp.get("/lista-cobros/<int:page>")
@login_required
@check("invoice_index")
def invoices_index(page,**order):
    if(len(order) != 0):
        invoices = utiles.select_filter(**order)
    else:
        invoices = utiles.select_all()
    invoices = db.paginate(invoices,page=page,max_per_page=10)
    return render_template("list_invoices.html", invoices=invoices)


@invoices_bp.post("/lista-cobros/")
@login_required
@check("invoice_index")
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
@login_required
@check("invoice_destroy")
def delete_invoice():
    id_delete = request.form['id']
    utiles.delete(id_delete)
    return redirect("/cobros/")


#Ruta para actualizar cobro
@invoices_bp.get("/actualizar-cobro/<int:invoice_id>")
@login_required
@check("invoice_update")
def update_invoice(invoice_id):
    invoice = utiles.get_invoice(invoice_id)
    return render_template("update_invoice.html",invoice=invoice)

@invoices_bp.post("/actualizar-cobro/<int:invoice_id>")
@login_required
@check("invoice_update")
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
@login_required
@check("invoice_new")
def invoice_create():
    jinetes_amazonas = utiles.get_all_ja()
    employees = utiles.get_all_employees()
    return render_template("create_invoice.html",invoices=invoices_bp,jinetes_amazonas=jinetes_amazonas,employees = employees)

@invoices_bp.post("/crear-cobro")
@login_required
@check("invoice_new")
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
@invoices_bp.get("/deudores/<int:page>")
@login_required
@check("invoice_index")
def invoice_statuses(page,**order):
    per_page = 5
    if(len(order) != 0):
        ja_query = crud_JyA.search_JYA(
            nombre=order["nombre"],
            apellido=order["apellido"],
            page=1,
            per_page=per_page
        )
    else:
        ja_query = utiles.get_all_ja()
        ja_query = db.paginate(ja_query,page=page,max_per_page=5)
    return render_template("statuses_list.html",invoices=invoices_bp,jinetes_amazonas=ja_query, page = page)


@invoices_bp.post("/deudores/<int:page>")
@login_required
@check("invoice_index")
def order_statuses_list(page):
    if("id" in request.form):
        return update_status(page)
    else:
        order_information = {
            "nombre": request.form['first_name'],
            "apellido": request.form['last_name'],
        }
        return invoice_statuses(page,**order_information)


@invoices_bp.post("/deudores/<int:page>")
@login_required
@check("invoice_update")
def update_status(page,**order):
    ja_update = request.form['id']
    utiles.change_status(ja_update)
    return invoice_statuses(page)

#rutas para la muestra de un cobro especifico.
@invoices_bp.get("/mostrar-cobro/<int:invoice_id>")
@login_required
@check("invoice_show")
def show_invoice(invoice_id):
    invoice = utiles.get_invoice(invoice_id)
    return render_template("show_invoice.html",invoice=invoice)
