from core.database import db
import enum
from sqlalchemy import Enum
"""
    modelo de cobros 
"""
class payment_methods(enum.Enum):
    name='payment_methods'
    efectivo:1
    tarjeta_credito:2
    tarjeta_debito:3
    otros:4

class Invoices(db.Model):
    __tablename__="invoices"
    id = db.Column(db.Integer, primary_key=True)
    j_a = db.Column(db.Integer, db.ForeignKey("users.id"))
    pay_date = db.Column(db.Date)
    payment_method = db.Column(Enum(payment_methods))
    amount = db.Column(db.Float)
    recipient = db.Column(db.Integer,db.ForeignKey("users.id"))
    observations = db.Column(db.Text, nullable=True)

