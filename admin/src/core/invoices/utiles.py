from core.database import db
from src.core.invoices.invoices import Invoices

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
        "efectivo",
        "tarjeta de credito",
        "tarjeta de debito",
        "otro"
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