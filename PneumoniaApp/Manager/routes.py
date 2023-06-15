from flask import Blueprint, render_template,  redirect, url_for, request, send_file
from flask_login import login_user, current_user, logout_user, login_required
from PneumoniaApp.Authentication.models import Patient, Doctor, Manager
from PneumoniaApp import db
from PneumoniaApp.Authentication.validate import *
from PneumoniaApp.Patient.models import *
import csv
import os

manager = Blueprint('manager', __name__)

@manager.route("/approveDoctors", methods=['POST','GET'])
@login_required
def approveDoctors():
    if request.method == 'POST':
        approved_doctors = request.form.getlist('doctors')
        for doctor_id in approved_doctors:
            doctor = Doctor.query.get(doctor_id)
            if doctor:
                doctor.is_approved = True
                db.session.commit()
        return redirect(url_for('manager.approveDoctors'))

    doctors = Doctor.query.filter_by(is_approved = False)
    return render_template('approveDoctors.html', doctors = doctors)

@manager.route("/waitingForDiagnose")
@login_required
def waitingForDiagnose():
    reports = Report.query.filter_by(is_answer=False)
    return render_template("ManagerDiagnoseHistory.html", reports=reports)

@manager.route("/report-details/<int:report_id>")
@login_required
def report_details(report_id):
    report = Report.query.get(report_id)
    if report:
        doctor = Doctor.query.filter_by(id=report.doctor_id).first()
        return render_template("ManagerReportDetails.html", report=report, doctor=doctor)
    else:
        return render_template("ManagerDiagnoseHistory.html", reports=reports)

@manager.route("/downloadReports")
@login_required
def downloadReports():
    reports = Report.query.filter_by(is_answer=False).all()
    filename = "waitForReports.csv"
    absolute_path = os.path.join(os.getcwd(), filename)

    with open(absolute_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Report ID", "Start Date", "Patient ID", "Patient Name", "Doctor ID", "Doctor Name"])
        for report in reports:
            user = Patient.query.filter_by(id=report.patient_id).first()
            doctor = Doctor.query.filter_by(id=report.doctor_id).first()

            writer.writerow([report.id, report.start_date, user.user_id, user.username, doctor.user_id, doctor.username])

    return send_file(absolute_path, as_attachment=True)