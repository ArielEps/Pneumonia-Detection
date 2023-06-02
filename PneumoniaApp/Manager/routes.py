from flask import Blueprint, render_template,  redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from PneumoniaApp.Authentication.models import Patient, Doctor, Manager
from PneumoniaApp import db
from PneumoniaApp.Authentication.validate import *

manager = Blueprint('manager', __name__)

@manager.route("/approveDoctors", methods=['POST','GET'])
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
