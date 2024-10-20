from core.database import db
from src.core.invoices.invoices import Invoices
from src.core.models.model_JyA import JYA
from sqlalchemy import desc

payment_methods_list = [
        "Efectivo",
        "Tarjeta de credito",
        "Tarjeta de debito",
        "Otro"
    ]

def create(**kwargs):
    invoice = Invoices(**kwargs)
    db.session.add(invoice)
    db.session.commit()
    return invoice

def delete(id_delete):
    db.session.query(Invoices).filter(Invoices.id==id_delete).delete()
    db.session.commit()

def validate_create(**datos):
    payment_method = datos.get("payment_method")
    if(not payment_method in payment_methods_list):
        return False
    if(datos.get("amount")<0):
        return False
    JYA.query.get_or_404(datos.get("j_a"))
    #empleados.query.get_or_404(datos.get("recipient"))
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
    
    return True

def get_all_ja():
    ja_query = JYA.query.all()
    ja_dictionary = {}
    for ja in ja_query:
        ja_dictionary[ja.id] = ja.nombre + " " + ja.apellido
    return ja_dictionary

def get_ja(ja_id):
    query = JYA.query.get_or_404(ja_id)
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

#De momento esta hecho con JYA porque queria probar como hacerlo. Cuando tenga para conectar con modelo de empleados cambiara.
def select_filter(**kwargs):
    invoices = db.select(Invoices)
    if(kwargs['date_from'] != '') and (kwargs['date_to'] !=''):
        invoices = invoices.filter(Invoices.pay_date.between(kwargs["date_from"],kwargs["date_to"]))
    if(kwargs['payment_method'] != ''):
        invoices = invoices.filter(Invoices.payment_method == kwargs['payment_method'])
    if(kwargs['first_name'] != ''):
        id_filter = db.select(JYA.id).filter(JYA.nombre == kwargs["first_name"])
        invoices = invoices.filter(Invoices.j_a.in_(id_filter))
    if(kwargs['last_name'] != ''):
        id_filter = db.select(JYA.id).filter(JYA.apellido==kwargs["last_name"])
        invoices = invoices.filter(Invoices.j_a.in_(id_filter))
    if(kwargs['order'] != ""):
        if(kwargs['order'] == 'ASC'):
            invoices = invoices.order_by((Invoices.pay_date))
        elif(kwargs['order'] =='DESC'):
            invoices = invoices.order_by(desc(Invoices.pay_date))
    return invoices

def select_all():
    return db.select(Invoices)