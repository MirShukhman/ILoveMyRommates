from .base_model import BaseModel
from . import db

class SetBill(BaseModel):
    __tablename__ = 'SetBills'
    
    SetBillName = db.Column(db.String(200), nullable=False)
    HomeID = db.Column(db.BigInteger, db.ForeignKey('Homes.ID'), nullable=False)
    Sum = db.Column(db.Numeric(precision=10, scale=2), nullable=False)