from core.database import db
import enum
from sqlalchemy import Enum

#Modelo de cobros
class Invoices(db.Model):
    __tablename__="invoices"
    id = db.Column(db.Integer, primary_key=True)
    #j_a = db.Column(db.Integer, db.ForeignKey("ja.id")) de momento por falta de modelo no es asi
    j_a = db.Column(db.Integer)
    pay_date = db.Column(db.Date)
    payment_method = db.Column(db.String)
    amount = db.Column(db.Float)
    #recipient = db.Column(db.Integer,db.ForeignKey("users.id")) de momento por falta de modelo no es asi
    recipient = db.Column(db.Integer)
    observations = db.Column(db.Text, nullable=True)


#Modelo para registrar deudores

class debt_statuses(db.Model):
        __tablename__="debt_statuses"
        id = db.Column(db.Integer, primary_key=True)
        """id_ja = db.COlumn(db.Integer, ForeignKey("ja.id"))"""
        id_ja = db.Column(db.Integer)
        debts = db.Column(db.Boolean, default=False)