from flask import Flask
from flask_bcrypt import Bcrypt

from models import db
from backend_logic.email_handler import EmailHandler

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('.config')
    db.init_app(app)
    bcrypt.init_app(app)
    
    return app


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        from models.bills import Bill
        from models.homes import Home
        from models.payments import Payment
        from models.set_bills import SetBill
        from models.tenants import Tenant
        from models.users import User
        db.create_all()
        
        # playground
        # 3 homes
        
        # 2 tennants per home (6 total) + 6 usrs 
        #add=User.add(TenantID= None, PasswordHash= '123', Username='test',Email='test')
        #print (add.ID)
        from backend_logic.login_token import LoginToken
        lt = LoginToken()
        lt.generate_token(1,1,1)
        
    app.run(debug=app.config['DEBUG'], use_reloader=app.config['USE_RELOADER'])
    