from PneumoniaApp.Authentication.models import Patient, Doctor, Manager

def check_if_patient_exist(id, email):
    patient_email = Patient.query.filter_by(email=email).first()
    patient_id = Patient.query.filter_by(user_id=id).first()

    if patient_email or patient_id:
        return True
    return False

def check_if_doctor_exist(id, email, doctor_license):
    doctor_email = Doctor().query.filter_by(email=email, user_id=id, doctor_license=doctor_license).first()
    doctor_id = Doctor().query.filter_by( user_id=id).first()
    doctor_license =Doctor().query.filter_by(doctor_license=doctor_license).first()
    
    if doctor_email or doctor_id or doctor_license:
        return True
    return False