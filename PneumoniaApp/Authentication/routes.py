from flask import Blueprint, render_template

Authentication = Blueprint('Authentication', __name__)

@Authentication.route("/")
def Hi():
    return "hello"