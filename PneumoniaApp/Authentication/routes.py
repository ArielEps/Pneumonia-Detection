from flask import Blueprint, render_template,  redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from PneumoniaApp.Authentication.models import Patient, Doctor, Manager
from PneumoniaApp import db
from PneumoniaApp.Authentication.validate import *
from flask_bcrypt import Bcrypt

Authentication = Blueprint('Authentication', __name__)
bcrypt = Bcrypt()

@Authentication.route("/", methods=['POST','GET'])
def Login():
    if request.method == 'POST':
        user_id = request.form.get('id')
        email = request.form.get('email')
        password = request.form.get('password')
        auth = request.form.get('select')

        if auth == 'Manager':
            
            manager = Manager.query.filter_by(email=email).first()
            
            if manager and bcrypt.check_password_hash(manager.password, password):
                login_user(manager, remember=False)
                return  redirect(url_for('Authentication.ManagerHome'))
            else:
                message = "incorrect field, please log again!" 
                return render_template('Login.html', message = message)


        elif auth == 'Patient':
            patient = Patient.query.filter_by(email=email).first()

            if patient and bcrypt.check_password_hash(patient.password, password):
                login_user(patient, remember=False)
                return  redirect(url_for('Authentication.patientHome'))
            else:
                message = "incorrect field, please log again!" 
                return render_template('Login.html', message = message)
        
        else:
            doctor = Doctor.query.filter_by(email=email).first()
            
            if doctor and bcrypt.check_password_hash(doctor.password, password):
                if doctor.is_approved:
                    login_user(doctor, remember=False)
                    return  redirect(url_for('Authentication.doctorHome'))
                else:
                    message = "Waiting for manager approval" 
                    return render_template('Login.html', message = message)
            else:
                message = "incorrect field, please log again!" 
                return render_template('Login.html', message = message)

    return render_template('Login.html')


@Authentication.route("/ChooseAuth")
def ChooseAuth():
    return render_template('ChooseAuth.html')

@Authentication.route("/DoctorRegister",  methods=['POST','GET'])
def DoctorRegister():
    if request.method == 'POST':
        username = request.form.get('username')
        user_id = request.form.get('id')
        email = request.form.get('email')
        password = request.form.get('password')
        license = request.form.get('license')

        if not check_if_doctor_exist(user_id, email, license):
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            doctor = Doctor(user_id=user_id, username=username,email=email, password=hashed_password,doctor_license=license)

            db.session.add(doctor)
            db.session.commit()
            return  redirect(url_for('Authentication.Login'))
    
        message = "User already exist"
        return render_template('DoctorRegister.html', message=message)
    return render_template('DoctorRegister.html')


@Authentication.route("/PatientRegister",  methods=['POST','GET'])
def PatientRegister():
    if request.method == 'POST':
        username = request.form.get('username')
        user_id = request.form.get('id')
        email = request.form.get('email')
        password = request.form.get('password')

        if not check_if_patient_exist(user_id, email):
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            patient = Patient(user_id=user_id, username=username,email=email, password=hashed_password)

            db.session.add(patient)
            db.session.commit()
            return  redirect(url_for('Authentication.Login'))
    
        message = "User already exist"
        return render_template('PatientRegister.html', message=message)
    return render_template('PatientRegister.html')

@Authentication.route("/managerHome")
@login_required
def ManagerHome():
    return render_template('ManagerHome.html')

@Authentication.route("/patientHome")
@login_required
def patientHome():
    return render_template('patientHome.html')

@Authentication.route("/doctorHome")
@login_required
def doctorHome():
    return render_template('doctorHome.html')

@Authentication.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Authentication.Login'))


@Authentication.route("/ManagerChangePassword",  methods=['POST','GET'])
@login_required
def ManagerChangePassword():
    if request.method == 'POST':
        password = request.form.get('password')
        confPass = request.form.get('passwordConf')
        if check_if_password(password, confPass):
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            manager = Manager.query.filter_by(id = current_user.id).first()
            manager.password = password
            db.session.commit()
            return redirect(url_for('Authentication.ManagerHome'))
        else:
            return render_template('ManagerchangePassword.html', message="password not match!")
            
    return render_template('ManagerchangePassword.html')

@Authentication.route("/PatientChangePassword",  methods=['POST','GET'])
@login_required
def PatientChangePassword():
    if request.method == 'POST':
        password = request.form.get('password')
        confPass = request.form.get('passwordConf')
        if check_if_password(password, confPass):
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            patient = Patient.query.filter_by(id = current_user.id).first()
            patient.password = password
            db.session.commit()
            return redirect(url_for('Authentication.patientHome'))
        else:
            return render_template('PatientchangePassword.html', message="password not match!")
        
    return render_template('PatientchangePassword.html')

@Authentication.route("/DoctorChangePassword",  methods=['POST','GET'])
@login_required
def DoctorChangePassword():
    if request.method == 'POST':
        password = request.form.get('password')
        confPass = request.form.get('passwordConf')
        if check_if_password(password, confPass):
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            doctor = Doctor.query.filter_by(id = current_user.id).first()
            doctor.password = password
            db.session.commit()
            return redirect(url_for('Authentication.doctorHome'))
        else:
            return render_template('DoctorchangePassword.html', message="password not match!")
    return render_template('DoctorchangePassword.html')
    
