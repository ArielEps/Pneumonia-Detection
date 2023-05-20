from flask import Blueprint, render_template,  redirect, url_for

Authentication = Blueprint('Authentication', __name__)


@Authentication.route("/")
def AuthScreen():
    return render_template('Login.html')