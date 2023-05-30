from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


db = SQLAlchemy()

def create_app(database_uri="sqlite:///site.db"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)


    from PneumoniaApp.Authentication.models import Patient, Doctor, Manager
    @login_manager.user_loader
    def load_user(user_id):
        patient = Patient.query.get(int(user_id))
        doctor = Doctor.query.get(int(user_id))
        manager = Manager.query.get(int(user_id))

        if patient:
            return patient
        elif doctor:
            return doctor
        else:
            return manager

    from PneumoniaApp.Authentication.routes import Authentication
    app.register_blueprint(Authentication)
    
    return app

app = create_app()
app.app_context().push()
db.create_all()