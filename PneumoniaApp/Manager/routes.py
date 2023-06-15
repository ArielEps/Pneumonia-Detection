from flask import Blueprint, render_template,  redirect, url_for, request, send_file
from flask_login import login_user, current_user, logout_user, login_required
from PneumoniaApp.Authentication.models import Patient, Doctor, Manager, UserActivity
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

@manager.route("/reports-details/<int:report_id>")
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


@manager.route("/downloadDiagnose")
@login_required
def downloadDiagnose():
    reports = Report.query.filter_by(is_answer=True).all()
    filename = "DiagnoseReports.csv"
    absolute_path = os.path.join(os.getcwd(), filename)

    with open(absolute_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Report ID", "Start Date", "End Date", "Patient ID", "Patient Name", "Doctor ID", "Doctor Name", "Helping Doctor ID", "Helping Doctor Name", "Helping Doctor Answer", "AI Help", "AI Answer", "Is Sick"])
        for report in reports:
            user = Patient.query.filter_by(id=report.patient_id).first()
            doctor = Doctor.query.filter_by(id=report.doctor_id).first()
            help_doctor = Doctor.query.filter_by(id=report.helping_doctor_id).first()
            
            writer.writerow([report.id, report.start_date, report.end_date, user.user_id, user.username, doctor.user_id, doctor.username, help_doctor.user_id if help_doctor else '', help_doctor.username if help_doctor else '', report.helping_doctor_answer if report.helping_doctor_answer is not None else '', report.ai_help, report.ai_answer, report.is_sick])

    return send_file(absolute_path, as_attachment=True)

@manager.route("/downloadLoginReports")
@login_required
def downloadLoginReports():
    activities = UserActivity.query.all()
    filename = "UserActivityReport.csv"
    absolute_path = os.path.join(os.getcwd(), filename)

    with open(absolute_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "User ID", "Username", "Login Date", "Logout Date"])
        for activity in activities:
            user = None
            if activity.user_id:
                user = Patient.query.filter_by(id=activity.user_id).first() or Doctor.query.filter_by(id=activity.user_id).first()
            
            writer.writerow([activity.id, user.user_id if user else '', user.username if user else '', activity.login_datetime, activity.logout_datetime])

    return send_file(absolute_path, as_attachment=True)


@manager.route("/downloadAppointmentReports")
@login_required
def downloadAppointmentReports():
    appointments = Appointment.query.all()
    filename = "AppointmentsReport.csv"
    absolute_path = os.path.join(os.getcwd(), filename)

    with open(absolute_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Created At", "Date", "Time", "Patient ID", "Patient name", "Doctor ID", "Doctor name"])
        for appointment in appointments:
            user = Patient.query.filter_by(id=appointment.patient_id).first()
            doctor = Doctor.query.filter_by(id=appointment.doctor_id).first()
            writer.writerow([appointment.id, appointment.created_at, appointment.date, appointment.time, user.user_id, user.username, doctor.user_id, doctor.username])

    return send_file(absolute_path, as_attachment=True)


@manager.route("/ManagerReports")
@login_required
def managerReports():
    return render_template("ManagerReports.html")