from .base_model import BaseModel
from . import db

class Payment(BaseModel):
    __tablename__ = 'Payments'
    
    PaiedBy = db.Column(db.BigInteger, db.ForeignKey('Tenants.ID'), nullable=False)
    PaiedTo = db.Column(db.BigInteger, db.ForeignKey('Tenants.ID'), nullable=False)
    BillID = db.Column(db.BigInteger, db.ForeignKey('Bills.ID'), nullable=False)
    PaymentDate = db.Column(db.DateTime, nullable=False)
    Sum = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    Image = db.Column(db.LargeBinary)
    ExternalID = db.Column(db.String(200))
    ApprovedByRecipient = db.Column(db.Boolean, nullable=False)