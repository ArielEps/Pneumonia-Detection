from flask import Blueprint, render_template,  redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from PneumoniaApp.Authentication.models import Patient, Doctor, Manager
from PneumoniaApp.Patient.models import Report, Appointment
from PneumoniaApp import db
from PneumoniaApp.Authentication.validate import *
import os
import secrets
from datetime import datetime, date
from werkzeug.utils import secure_filename

patient = Blueprint('patient', __name__)


@patient.route("/PatientDiagnose", methods=['POST', 'GET'])
@login_required
def PatientDiagnose():
    if request.method == 'POST':
        file = request.files['file']
        doctor = request.form.get('doctor')

        images_folder = os.path.join("PneumoniaApp", "static", "Images")
        os.makedirs(images_folder, exist_ok=True)

        filename = secure_filename(file.filename)
        file_path = os.path.join(images_folder, filename)
        file.save(file_path)

        report = Report(image=file.filename, patient_id=current_user.id, doctor_id=doctor)
        db.session.add(report)
        db.session.commit()
        return redirect(url_for('Authentication.patientHome'))

    doctor = Doctor.query.filter_by(is_approved=True)
    return render_template("PatientDiagnoseReport.html", doctor=doctor)


@patient.route("/DiagnoseHistory")
@login_required
def DiagnoseHistory():
    reports = Report.query.filter_by(patient_id=current_user.id, is_answer=True)
    return render_template("PatientDiagnoseHistory.html", reports=reports)

@patient.route("/DiagnoseReport")
@login_required
def DiagnoseReport():
    reports = Report.query.filter_by(patient_id=current_user.id, is_answer=False)
    return render_template("PatientDiagnoseHistory.html", reports=reports)

@patient.route("/report-details/<int:report_id>")
@login_required
def report_details(report_id):
    report = Report.query.get(report_id)
    if report:
        doctor = Doctor.query.filter_by(id=report.doctor_id).first()
        return render_template("patientReportDetails.html", report=report, doctor=doctor)
    else:
        return render_template("PatientDiagnoseHistory.html", reports=reports)


@patient.route("/PatientScedule", methods=['POST', 'GET'])
@login_required
def PatientScedule():
    if request.method == 'POST':
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        doctor_id = int(request.form.get('doctor'))
        
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        
        appointment = Appointment(date=date_obj, time=time_obj, patient_id=current_user.id, doctor_id=doctor_id)
        db.session.add(appointment)
        db.session.commit()

    doctor = Doctor.query.filter_by(is_approved=True).all()
    return render_template("PatientScedule.html", doctor=doctor)