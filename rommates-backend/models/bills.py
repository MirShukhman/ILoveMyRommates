from .base_model import BaseModel
from . import db

class Bill(BaseModel):
    __tablename__ = 'Bills'
    
    BillName = db.Column(db.String(200), nullable=False)
    BillDate = db.Column(db.DateTime, nullable=False)
    Sum = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    PayedBy = db.Column(db.BigInteger, db.ForeignKey('Tenants.ID'))
    HomeID = db.Column(db.BigInteger, db.ForeignKey('Homes.ID'), nullable=False)
    Image = db.Column(db.LargeBinary)
    ExternalID = db.Column(db.String(200))
    SetBillID = db.Column(db.BigInteger, db.ForeignKey('SetBills.ID'))