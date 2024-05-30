from .base_model import BaseModel
from . import db

class Notification(BaseModel):
    __tablename__ = 'Notifications'
    
    UserID = db.Column(db.BigInteger, db.ForeignKey('Users.ID'))
    Message = db.Column(db.Text, nullable=False)
    IsRead = db.Column(db.Boolean, default=False)
    CreatedAt = db.Column(db.DateTime, nullable=False)
