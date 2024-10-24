from src.core.database import db
import enum
from sqlalchemy import Enum, ForeignKey

#Modelo de cobros
class Invoices(db.Model):
    __tablename__="invoices"
    id = db.Column(db.Integer, primary_key=True)
    j_a = db.Column(db.Integer, db.ForeignKey("JYA.id"))
    pay_date = db.Column(db.Date)
    payment_method = db.Column(db.String)
    amount = db.Column(db.Float)
    recipient = db.Column(db.Integer,db.ForeignKey("empleados.id"))
    observations = db.Column(db.Text, nullable=True)


