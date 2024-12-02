from flask import flash
from src.core.database import db
from src.core.invoices.invoices import Invoices
from src.core.auth.models.model_JyA import JYA
from src.core.auth.models.model_empleado import Empleados
from sqlalchemy import desc

payment_methods_list = [
        "Efectivo",
        "Tarjeta de credito",
        "Tarjeta de debito",
        "Otro"
    ]

def create(**kwargs):
    """
        Crea un cobro.
        Mediante el id de j&a y empleado consigue los nombres y apellidos de cada uno y los agrega en un cobro a la bd.

        Returns:
            el cobro creado
    """
    j_a = JYA.query.get_or_404(kwargs['j_a'])
    emp = Empleados.query.get_or_404(kwargs['recipient'])
    kwargs['ja_first_name'] = j_a.nombre
    kwargs['ja_last_name'] = j_a.apellido
    kwargs['recipient_first_name'] = emp.nombre
    kwargs['recipient_last_name'] = emp.apellido
    del kwargs['j_a']
    del kwargs['recipient']
    invoice = Invoices(**kwargs)
    db.session.add(invoice)
    db.session.commit()
    return invoice

def delete(id_delete):
    """
        Elimina un cobro mediante id.
        Args:
            id_delete(int): Id del cobro a eliminar
        Returns:
            None
    """
    db.session.query(Invoices).filter_by(id=id_delete).delete()
    db.session.commit()

def validate_create(**datos):
    """
        Valida los datos recibidos.
        Args: 
            **datos: Datos a validar.
        Returns:
            bool: True si los datos son validos, False en caso contrario.
    """
    payment_method = datos.get("payment_method")
    if(not payment_method in payment_methods_list):
        return False
    if(datos.get("amount")<0):
        return False
    return True 

def get_invoice(id):
    """
        Obtiene un cobro mediante id, si no lo encuentra devuelve un error 404.
        Args:
            id(int): Id del cobro a buscar.
        Returns:
            Cobro obtenido o error 404. 
    """
    return Invoices.query.get_or_404(id)

def validate_update(**kwargs):
    """
        Valida los datos obtenidos en una actualización.
        Args:
            **kwargs:Datos a validar.
        Returns:
            True en caso de ser validados como correcto. False en caso contrario.
    """
    payment_method = kwargs.get("payment_method")
    amount = kwargs.get("amount")
    if(payment_method != ''):
        if(not payment_method in payment_methods_list):
            return False
    if(amount != ''):
        if(float(amount) < 0):
            return False
    return True

def update_invoice(invoice_id,**kwargs):
    """
        Actualiza un cobro en la BD.
        Llama a una funcion para validar los datos. Si son correctos actualiza y crea un mensaje de exito.
        Args:
            invoice_id(int): Id del cobro a actualizar.
            **kwargs: Datos con los que actualizar al cobro.
        Returns:
            True si los datos son validos. False en caso contrario.
    """
    invoice = get_invoice(invoice_id)
    if(validate_update(**kwargs)):
        for key, value in kwargs.items():
            if value != '':
                setattr(invoice, key, value)

        db.session.commit()
    else:
        return False
    flash("Se actualizo con exito un cobro",'true')
    return True

def get_all_ja():
    """
        Consigue un listado de todos los JYA ordenados por apellido.
        Returns:
            Listado de JYA ordenados por apellido.
    """
    ja_query = JYA.query.filter(JYA.eliminado == False).order_by(JYA.apellido)
    return ja_query

def get_all_employees():
    """
        Consigue un listado de todos los empleados ordenados por apellido.
        Returns:
            Listado de empleados ordenados por apellido.
    """
    emp_query = Empleados.query.order_by(Empleados.apellido)
    return emp_query

def get_emp(emp_id):
    """
        Obtiene el nombre y apellido de un empleado.
        Realiza una consulta para obtener un empleado por id y retorna nombre y apellido del mismo.
        Args:
            emp_id(int):Id del empleado a buscar
        Returns:
            String de nombre y apellido concatenados separados por un espacio.
    """
    query = Empleados.query.get_or_404(emp_id)
    return query.nombre + " " + query.apellido

def get_statuses():
    """
        Genera un diccionario con los estados de deuda de los J&A.
        Realiza una consulta para obtener un listado de los J&A y arma un diccionario con id y estado de deuda de cada uno.
        Returns:
            Diccionario con estado de deudas de JYA e indices con sus ID.
    """
    status_query = JYA.query.all()
    status_dictionary = {}
    for status in status_query:
        status_dictionary[status.id] = status.debts
    return status_dictionary

def change_status(id_change):
    """
        Cambia el estado de deudor de un J&A
        Args:
            id_change(int):Id del J&A a ser actualizado.
        Returns:
            None
    """
    query_value = JYA.query.get_or_404(id_change)
    setattr(query_value,'debts',not query_value.debts)
    db.session.commit()

def get_recipients():
    pass

def select_filter(**kwargs):
    """
        Listar cobros con filtro.
        Recibe argumentos por los que filtrar y si se encuentran realiza filtros a un select de cobros.
        Args:
            Kwargs:Filtros a realizar.
        Returns:
            Listado de cobros.
    """
    invoices = db.select(Invoices)
    if(kwargs['date_from'] != ''):
        invoices = invoices.filter(Invoices.pay_date >= kwargs["date_from"])
    if(kwargs['date_to'] != ''):
        invoices = invoices.filter(Invoices.pay_date <= kwargs["date_to"])
    if(kwargs['payment_method'] != ''):
        invoices = invoices.filter(Invoices.payment_method == kwargs['payment_method'])
    if(kwargs['first_name'] != ''):
        first_name_filter = db.select(Empleados.nombre).filter(Empleados.nombre == kwargs["first_name"])
        invoices = invoices.filter(Invoices.recipient_first_name.in_(first_name_filter))
    if(kwargs['last_name'] != ''):
        last_name_filter = db.select(Empleados.apellido).filter(Empleados.apellido==kwargs["last_name"])
        invoices = invoices.filter(Invoices.recipient_last_name.in_(last_name_filter))
    if(kwargs['order'] != ""):
        if(kwargs['order'] == 'ASC'):
            invoices = invoices.order_by((Invoices.pay_date))
        elif(kwargs['order'] =='DESC'):
            invoices = invoices.order_by(desc(Invoices.pay_date))
    return invoices

def select_all():
    """
        Realiza un listado de todos los cobros
        Returns:
            Lista de todos los cobros.
    """
    return db.select(Invoices)

def filtrar_cobros(empleado_id, fecha_inicio, fecha_fin):
    """
        Filtrado de cobros. 
        Realiza un filtrado de cobros mediante id de empleado y fecha desde y hasta.
        Args:
            empleado_id(int):Empleado a buscar
            fecha_inicio(date):Fecha desde la que buscar.
            fecha_fin(date):Fecha hasta la que buscar.
        Returns:
            Lista de cobros filtrada.    
    """
    return Invoices.query.join(
        Empleados, 
        (Empleados.nombre == Invoices.recipient_first_name) & 
        (Empleados.apellido == Invoices.recipient_last_name)
    ).filter(
        Invoices.pay_date >= fecha_inicio,
        Invoices.pay_date <= fecha_fin,
        Empleados.id == empleado_id
    ).all()

    
def get_empleados_con_cobros():
    """
        Obtiene una lista de empleados que figuran en cobros.
        Returns:
            Lista de empleados que figuran en cobros.
    """
    empleados_cobradores = db.session.query(Empleados).join(
        Invoices, 
        (Empleados.nombre == Invoices.recipient_first_name) &
        (Empleados.apellido == Invoices.recipient_last_name)
    ).distinct().all()

    return empleados_cobradores


def search_cobros(
    recipient_first_name=None, 
    recipient_last_name=None, 
    payment_method=None, 
    date_from=None, 
    date_to=None, 
    order='asc', 
    page=1, 
    per_page=10
):
    """
    Busca cobros en la base de datos aplicando varios filtros.

    Args:
        recipient_first_name: Nombre del usuario a buscar.
        recipient_last_name: Apellido del usuario a buscar.
        payment_method: Forma de pago del cobro.
        date_from: Fecha inicial para filtrar cobros.
        date_to: Fecha final para filtrar cobros.
        order: Orden de la lista ('asc' o 'desc').
        page: Página de resultados (por defecto es 1).
        per_page: Número de resultados por página (por defecto es 10).

    Returns:
        Objeto de paginación con los cobros encontrados.
    """
    query = Invoices.query

    if recipient_first_name:
        query = query.filter(Invoices.recipient_first_name.ilike(f"%{recipient_first_name}%"))

    if recipient_last_name:
        query = query.filter(Invoices.recipient_last_name.ilike(f"%{recipient_last_name}%"))

    if payment_method:
        query = query.filter_by(payment_method=payment_method)

    if date_from:
        query = query.filter(Invoices.pay_date >= date_from)
    if date_to:
        query = query.filter(Invoices.pay_date <= date_to)

    if order == 'asc':
        query = query.order_by(Invoices.pay_date.asc())
    else:
        query = query.order_by(Invoices.pay_date.desc())

    return query.paginate(page=page, per_page=per_page, error_out=False)
