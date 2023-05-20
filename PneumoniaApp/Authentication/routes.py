from flask import Blueprint, render_template,  redirect, url_for

Authentication = Blueprint('Authentication', __name__)


@Authentication.route("/")
def Login():
    return render_template('Login.html')


@Authentication.route("/ChooseAuth")
def ChooseAuth():
    return render_template('ChooseAuth.html')

@Authentication.route("/DoctorRegister",  methods=['POST','GET'])
def DoctorRegister():
    return render_template('DoctorRegister.html')

@Authentication.route("/PatientRegister",  methods=['POST','GET'])
def PatientRegister():
    return render_template('PatientRegister.html')