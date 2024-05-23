from .base_model import BaseModel
from . import db

class Tenant(BaseModel):
    __tablename__ = 'Tenants'
    
    Name = db.Column(db.String(200), nullable=False)
    HomeID = db.Column(db.BigInteger, db.ForeignKey('Homes.ID'), nullable=False)
    PaymentPart = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    CanEdit = db.Column(db.Boolean, nullable=False)
    JoinedAt = db.Column(db.DateTime, nullable=False)