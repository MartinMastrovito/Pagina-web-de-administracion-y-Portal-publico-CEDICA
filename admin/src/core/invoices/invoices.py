from src.core.database import db
import enum
from sqlalchemy import Enum, ForeignKey

class Invoices(db.Model):
    __tablename__="invoices"
    id = db.Column(db.Integer, primary_key=True)
    ja_first_name = db.Column(db.String)
    ja_last_name = db.Column(db.String)
    pay_date = db.Column(db.Date)
    payment_method = db.Column(db.String)
    amount = db.Column(db.Float)
    recipient_first_name = db.Column(db.String)
    recipient_last_name = db.Column(db.String)
    observations = db.Column(db.Text, nullable=True)


