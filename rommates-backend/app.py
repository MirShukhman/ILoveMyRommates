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
        from models.tokens import Token
        from models.notifications import Notification
        db.create_all()
        
        # playground
        from facades.unlogged import Unlogged
        unlogged = Unlogged()
        #print(unlogged.sign_up_first_step("test","test","miriamsh888@gmail.com",555,None))
        #print(unlogged.sign_up_second_step("miriamsh888@gmail.com",443286))
        #print(unlogged.reset_password("miriamsh888@gmail.com",682841,'888'))
        
                
    app.run(debug=app.config['DEBUG'], use_reloader=app.config['USE_RELOADER'])
    