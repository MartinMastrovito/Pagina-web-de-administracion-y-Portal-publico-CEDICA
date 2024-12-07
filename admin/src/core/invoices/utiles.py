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
    db.session.query(Invoices).filter_by(id=id_delete).delete()
    db.session.commit()

def validate_create(**datos):
    payment_method = datos.get("payment_method")
    if(not payment_method in payment_methods_list):
        return False
    if(datos.get("amount")<0):
        return False
    return True 

def get_invoice(id):
    return Invoices.query.get_or_404(id)

def validate_update(**kwargs):
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
    invoice = get_invoice(invoice_id)
    # Actualizar los atributos del usuario con los valores proporcionados en kwargs
    if(validate_update(**kwargs)):
        for key, value in kwargs.items():
            if value != '':
                setattr(invoice, key, value)
        
        # Confirmar los cambios en la base de datos
        db.session.commit()
    else:
        return False
    flash("Se actualizo con exito un cobro",'true')
    return True
#Modulo para conseguir el nombre de todos los JYA 
def get_all_ja():
    ja_query = JYA.query.order_by(JYA.apellido)
    return ja_query



#Modulo para conseguir el nombre de todos los empleados 
def get_all_employees():
    emp_query = Empleados.query.order_by(Empleados.apellido)
    return emp_query

#Modulo para conseguir el nombre de un empleado por su ID 
def get_emp(emp_id):
    query = Empleados.query.get_or_404(emp_id)
    return query.nombre + " " + query.apellido

def get_statuses():
    status_query = JYA.query.all()
    status_dictionary = {}
    for status in status_query:
        status_dictionary[status.id] = status.debts
    return status_dictionary

def change_status(id_change):
    query_value = JYA.query.get_or_404(id_change)
    setattr(query_value,'debts',not query_value.debts)
    db.session.commit()

def get_recipients():
    pass

def select_filter(**kwargs):
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
    return db.select(Invoices)

def filtrar_cobros(empleado_id, fecha_inicio, fecha_fin):
    return Invoices.query.filter(
        Invoices.recipient == empleado_id,
        Invoices.pay_date >= fecha_inicio,
        Invoices.pay_date <= fecha_fin
    ).all()
    
def get_empleados_con_cobros():
    empleados_cobradores = db.session.query(Empleados).join(
        Invoices, Empleados.dni == Invoices.recipient
    ).distinct().all()

    return empleados_cobradores