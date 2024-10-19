from core.database import db
from src.core.invoices.invoices import Invoices
from src.core.models.model_JyA import JYA


def create(**kwargs):
    invoice = Invoices(**kwargs)
    db.session.add(invoice)
    db.session.commit()
    return invoice

def delete(id_delete):
    db.session.query(Invoices).filter(Invoices.id==id_delete).delete()
    db.session.commit()

def validate(**datos):
    payment_methods_list = [
        "Efectivo",
        "Tarjeta de credito",
        "Tarjeta de debito",
        "Otro"
    ]
    payment_method = datos.get("payment_method")
    if(not payment_method in payment_methods_list):
        return False
    if(datos.get("amount")<0):
        return False
    return True 

def get_invoice(id):
    return Invoices.query.get_or_404(id)

def update_invoice(invoice_id,**kwargs):
    invoice = get_invoice(invoice_id)
    # Actualizar los atributos del usuario con los valores proporcionados en kwargs
    for key, value in kwargs.items():
        setattr(invoice, key, value)
    
    # Confirmar los cambios en la base de datos
    db.session.commit()
    
    return invoice

def get_ja():
    ja_query = JYA.query.all()
    ja_dictionary = {}
    for ja in ja_query:
        ja_dictionary[ja.id] = ja.nombre + " " + ja.apellido
    return ja_dictionary

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
