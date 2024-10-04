from core.database import db
from datetime import datetime

class payment_methods(payment_methods):
    cash = "efectivo"
    credit_card = "tarjeta de credito"
    debit_card = "tarjeta de débito"
    others = "otros"

class Invoices(db.Model):
    __tablename__="invoices"
    id = db.Column(db.Integer, primary_key=True)
    j_a = db.Column(db.Integer, db.ForeignKey("user.id"))
    pay_date = db.Column(db.Date)
    payment_method = db.Column()
    amount = db.Column(db.Decimal)
    recipient = db.Column(db.Integer,db.ForeignKey("user.id"))
    observations = db.Column(db.Text)

