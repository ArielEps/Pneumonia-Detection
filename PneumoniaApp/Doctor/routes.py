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

doctor = Blueprint('doctor', __name__)



@doctor.route("/DoctorsAppointments")
@login_required
def DoctorsAppointments():
    current_date = date.today()
    appointment = Appointment.query.filter(Appointment.doctor_id == current_user.id, Appointment.date >= current_date)
    patients = Patient.query.all()

    return render_template("DoctorsAppointments.html", appointments = appointment, pat = patients)

@doctor.route("/SearchPatientHistory", methods=['POST', 'GET'])
@login_required
def SearchPatientHistory():
    if request.method == 'POST':
        patient_id = request.form.get('search')

        patient = Patient.query.filter_by(user_id= patient_id).first()
        if patient != None:
            reports = Report.query.filter_by(patient_id=patient.id, is_answer=True)
            return render_template("DoctorPatientShowHistory.html", reports = reports)
        else:
            return render_template("DoctorPatientHistory.html", message = "Not such Patient")

    return render_template("DoctorPatientHistory.html")

@doctor.route("/Doctor_report-details/<int:report_id>")
@login_required
def Doctor_report_details(report_id):
    report = Report.query.get(report_id)
    if report:
        doctor = Doctor.query.filter_by(id=report.doctor_id).first()
        return render_template("DoctorReportDetails.html", report=report, doctor=doctor)
    else:
        return render_template("DoctorPatientHistory.html")