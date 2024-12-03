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

@invoices_bp.get("/")
@login_required
@check("invoice_index")
def invoices_index():
    """
    Ruta para mostrar la lista de cobros con paginación y filtrado.

    Returns:
        Renderiza la plantilla con la lista de cobros.
    """
    recipient_first_name = request.args.get('recipient_first_name')
    recipient_last_name = request.args.get('recipient_last_name')    
    payment_method = request.args.get('payment_method')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    order = request.args.get('order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    cobros_pagination = utiles.search_cobros(
        recipient_first_name=recipient_first_name,
        recipient_last_name=recipient_last_name,
        payment_method=payment_method,
        date_from=date_from,
        date_to=date_to,
        order=order,
        page=page,
        per_page=per_page
    )

    return render_template(
        "list_invoices.html",
        cobros=cobros_pagination.items,
        pagination=cobros_pagination,
    )

@invoices_bp.post("/eliminar/<int:cobro_id>")
@login_required
@check("invoice_destroy")
def delete_invoice(cobro_id):
    """
    Ruta para eliminar un cobro.

    Elimina un cobro identificado por su ID y redirige a la lista de cobros.

    Args:
        cobro_id (int): ID del cobro a eliminar.

    Returns: Redireccion a lista de cobros.
    """
    utiles.delete(cobro_id)
    flash("Se elimino el cobro","success")
    return redirect("/cobros")


@invoices_bp.get("/actualizar-cobro/<int:invoice_id>")
@login_required
@check("invoice_update")
def update_invoice(invoice_id):
    """
    Ruta para mostrar el formulario para actualizar un cobro.

    Obtiene los datos de un cobro identificado por su ID y los envía al template para su edición.

    Args:
        invoice_id (int): ID del cobro a actualizar.

    Returns:
        El contenido HTML de la página con el formulario de actualización junto al cobro a actualizar.
    """
    invoice = utiles.get_invoice(invoice_id)
    return render_template("update_invoice.html",invoice=invoice)

@invoices_bp.post("/actualizar-cobro/<int:invoice_id>")
@login_required
@check("invoice_update")
def invoice_update(invoice_id):
    """
    Ruta para actualizar la información de un cobro.

    Recibe los datos del formulario, actualiza el cobro identificado por su ID y redirige al listado de cobros.

    Args:
        invoice_id (int): ID del cobro a actualizar.

    Returns: Redireccion a lista de cobros
    """
    invoice_information = {
        "pay_date":request.form['pay_date'],
        "amount":(request.form['amount']),
        "observations":request.form['observations'],
        "payment_method":request.form['payment_method']
    }
    utiles.update_invoice(invoice_id, **invoice_information)
    return redirect("/cobros/")

@invoices_bp.get("/crear-cobro")
@login_required
@check("invoice_new")
def invoice_create():
    """
    Ruta para mostrar el formulario para crear un nuevo cobro.

    Obtiene la lista de jinetes/amazonas y empleados para enviarlos al template de creación de cobros.

    Returns:
        El contenido HTML de la página con el formulario de creación de cobros junto a los listados de j&a, empleados y el blueprint de cobros.
    """
    jinetes_amazonas = utiles.get_all_ja()
    employees = utiles.get_all_employees()
    return render_template("create_invoice.html",invoices=invoices_bp,jinetes_amazonas=jinetes_amazonas,employees = employees)

@invoices_bp.post("/crear-cobro")
@login_required
@check("invoice_new")
def create_invoice():
    """
    Ruta para crear un nuevo cobro.

    Recibe los datos del formulario, valida la información y crea un cobro y mensaje de exito si es válido.
    Sino, crea un mensaje de error.

    Returns:
        redireccion a pagina para crear cobros o redireccion a pagina de listado de cobros.
    """               
    invoice_information = {
        "pay_date": request.form['pay_date'],
        "amount": float(request.form['amount']),
        "payment_method": request.form['payment_method'],
        "j_a": int(request.form['j&a']),
        "recipient": int(request.form['recipient']),
        "observations": request.form['observations'],
    }
    if(utiles.validate_create(**invoice_information)):
         utiles.create(**invoice_information)
         flash("Se logro crear el cobro","success")
    else: 
        flash("No se pudo crear el cobro","error")
        return redirect('/cobros/crear-cobro')
    return redirect('/cobros')

@invoices_bp.get("/deudores/<int:page>")
@login_required
@check("invoice_index")
def invoice_statuses(page,**order):
    """
    Ruta para Listar el estado de deuda de los J&A.
    Args:
        page (int): Número de página para la paginación.
        **order: Opcional, parámetros de búsqueda para filtrar jinetes/amazonas.

    Returns:
        El contenido HTML de la página con la lista de estados de deuda.
    """
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
    """
    Ruta que recibe el orden para el listado de estado de deuda de los J&A
    Args: 
        page(int): Numero actual de pagina
    Returns:
        Funcion invoice_statuses con los parametros de pagina actual y de orden.
    """
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
    """
    Ruta para actualizar el estado de deuda de un J&A
    Args: 
        page(int): Numero actual de pagina
        **order: Opcional, parámetros de búsqueda para filtrar jinetes/amazonas. (Quedo sin usar :l)
    Returns:
        Funcion invoice_statuses con la pagina actual
    """
    ja_update = request.form['id']
    utiles.change_status(ja_update)
    return invoice_statuses(page)

@invoices_bp.get("/mostrar-cobro/<int:invoice_id>")
@login_required
@check("invoice_show")
def show_invoice(invoice_id):
    """
    Ruta para mostrar un cobro
    Args: 
       invoice_id(int): id del cobro a mostrar
    Returns:
        Contenido HTML para mostrar un cobro junto al cobro a mostrar.
    """
    invoice = utiles.get_invoice(invoice_id)
    return render_template("show_invoice.html",invoice=invoice)
