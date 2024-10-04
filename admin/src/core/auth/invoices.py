from core.database import db
from datetime import datetime

class Invoices(db.Model):
    __tablename__="invoices"
    id = db.Column(db.Integer, primary_key=True)
    pay_date = db.Column(db.Date)
    amount = db.Column(db.Decimal)
    observations
