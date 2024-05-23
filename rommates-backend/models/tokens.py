from .base_model import BaseModel
from . import db

class Token(BaseModel):
    __tablename__ = 'Tokens'
    
    UserID = db.Column(db.BigInteger, db.ForeignKey('Users.ID'))
    Token = db.Column(db.String(200), nullable=False)
    CreatedAt = db.Column(db.DateTime, nullable=False)
    ExpiresAt = db.Column(db.DateTime, nullable=False)