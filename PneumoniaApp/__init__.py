from flask import Flask

app = Flask(__name__)

from PneumoniaApp.Authentication.routes import Authentication
app.register_blueprint(Authentication)