from core.database import db
from datetime import datetime
"""
    modelo de cobros 
"""
#lass Payment_methods(Payment_methods):
#    cash = "efectivo"
#    credit_card = "tarjeta de credito"
#    debit_card = "tarjeta de débito"
#    others = "otros"

class Invoices(db.Model):
    __tablename__="invoices"
    id = db.Column(db.Integer, primary_key=True)
    j_a = db.Column(db.Integer, db.ForeignKey("users.id"))
    pay_date = db.Column(db.Date)
    payment_method = db.Column(db.Text)
    amount = db.Column(db.Float)
    recipient = db.Column(db.Integer,db.ForeignKey("users.id"))
    observations = db.Column(db.Text)

