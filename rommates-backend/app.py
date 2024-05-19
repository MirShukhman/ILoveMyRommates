from flask import Flask
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('.config')
    db.init_app(app)
    from models.base_model import BaseModel
    
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
        
    app.run(debug=app.config['DEBUG'], use_reloader=app.config['USE_RELOADER'])