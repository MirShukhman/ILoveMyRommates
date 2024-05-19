from .base_model import BaseModel
from . import db

class Home(BaseModel):
    __tablename__ = 'Homes'
    
    HomeName = db.Column(db.String(50), nullable=False)
    CreatedAt = db.Column(db.DateTime, nullable=False)
    BillingDate = db.Column(db.DateTime, nullable=False)
    IsActive = db.Column(db.Boolean, nullable=False)
    