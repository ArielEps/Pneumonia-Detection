from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os


db = SQLAlchemy()

def create_app(database_uri="sqlite:///site.db"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    db.init_app(app)
    bcrypt = Bcrypt(app)

    from PneumoniaApp.Authentication.routes import Authentication
    app.register_blueprint(Authentication)
    
    return app