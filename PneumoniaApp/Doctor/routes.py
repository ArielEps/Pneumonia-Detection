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

@doctor.route("/DoctorAnswer")
@login_required
def Doctor_Answer():
    return render_template("DoctorAnswer.html")

@doctor.route("/AnswerDiagnose")
@login_required
def AnswerDiagnose():
    reports = Report.query.filter_by(doctor_id = current_user.id, is_answer=False)
    return render_template("DoctorAnswerDiagnose.html", reports = reports)

@doctor.route("/Doctor_answer-details/<int:report_id>" , methods=['POST', 'GET'])
@login_required
def Doctor_answer_details(report_id):
    report = Report.query.get(report_id)
    if report:
        if request.method == 'POST':
            current_date = date.today()
            answer = request.form.get('select')

            answer = True if answer == 'Yes' else False

            report.is_answer = True
            report.is_sick = answer
            report.end_date = current_date

            db.session.commit()
            return redirect(url_for('Authentication.doctorHome'))

        doctor = Doctor.query.filter_by(id=report.doctor_id).first()
        return render_template("DoctorAnswerDetails.html", report=report)
    else:
        reports = Report.query.filter_by(doctor_id = current_user.id, is_answer=False)
        return render_template("DoctorAnswerDiagnose.html", reports = reports)
    
@doctor.route("/RequestHelp", methods=['POST', 'GET'])
@login_required
def RequestHelp():
    if request.method == 'POST':
        selected_reports = request.form.getlist('checkbox')
        doctor = request.form.get('select')
        
        for report in selected_reports:
            repo = Report.query.filter_by(id=report, is_answer=False).first()
            repo.helping_doctor_id = doctor
            db.session.commit()

    doctors = Doctor.query.filter_by(is_approved=True).all()
    reports = Report.query.filter_by(doctor_id=current_user.id, is_answer=False).all()
    return render_template("DoctorHelpDiagnose.html", reports=reports, doctors=doctors)



@doctor.route("/HelpingDoctors")
@login_required
def Helping_Doctors():
    return render_template("HelpingDoctors.html")


@doctor.route("/HelpingDoctor")
@login_required
def HelpDoctor():
    reports = Report.query.filter_by(helping_doctor_id = current_user.id, is_answer=False, helping_doctor_answer=None)
    return render_template("HelpingDoctorsDiagnose.html", reports = reports)



@doctor.route("/Doctor_help-details/<int:report_id>" , methods=['POST', 'GET'])
@login_required
def Doctor_Help_details(report_id):
    report = Report.query.get(report_id)
    if report:
        if request.method == 'POST':
            answer = request.form.get('select')

            answer = True if answer == 'Yes' else False

            report.helping_doctor_answer = answer
            

            db.session.commit()
            return redirect(url_for('Authentication.doctorHome'))

        doctor = Doctor.query.filter_by(id=report.doctor_id).first()
        return render_template("DoctorAnswerDetails.html", report=report)
    else:
        reports = Report.query.filter_by(helping_doctor_id = current_user.id, is_answer=False, helping_doctor_answer=None)
        return render_template("HelpingDoctorsDiagnose.html", reports = reports)


@doctor.route("/SeeAnswers")
@login_required
def SeeAnswers():
    reports = Report.query.filter(Report.doctor_id == current_user.id, Report.is_answer == False, Report.helping_doctor_answer != None).all()
    return render_template("DoctorsSeeAnswers.html", reports=reports)


@doctor.route("/Doctor_seeAnswers-details/<int:report_id>" , methods=['POST', 'GET'])
@login_required
def Doctor_SeeAnswer_details(report_id):
    report = Report.query.get(report_id)
    if report:
        doctor = Doctor.query.filter_by(id=report.helping_doctor_id).first()
        return render_template("DoctorSeeReport.html", report=report, doctor=doctor)
    else:
        reports = Report.query.filter(Report.doctor_id == current_user.id, Report.is_answer == False, Report.helping_doctor_answer != None).all()
        return render_template("DoctorsSeeAnswers.html", reports=reports)
    