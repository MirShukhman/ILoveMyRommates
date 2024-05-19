from .base_model import BaseModel
from . import db

class User(BaseModel):
    __tablename__ = 'Users'
    
    TenantID = db.Column(db.BigInteger, db.ForeignKey('Tenants.ID'))
    PasswordHash = db.Column(db.String(200), nullable=False)
    Username = db.Column(db.String(50), nullable=False, unique=True)
    Token = db.Column(db.String(200))
    Email = db.Column(db.String(100), nullable=False, unique=True)
    PhoneNum =  db.Column(db.Integer)
    ProfilePic = db.Column(db.LargeBinary)
