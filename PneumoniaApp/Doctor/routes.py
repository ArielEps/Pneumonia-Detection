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