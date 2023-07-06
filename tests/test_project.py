from PneumoniaApp.Authentication.models import *
from PneumoniaApp.Patient.models import *
from PneumoniaApp.Authentication.routes import bcrypt
from PneumoniaApp.Authentication.validate import *
from flask_login import login_user
from werkzeug.datastructures import FileStorage
from flask import url_for
from datetime import datetime, date
import os
import csv
from flask import Flask
from flask_login import LoginManager
from flask.testing import FlaskClient
from unittest.mock import patch, Mock
############################################################################################# pages tests ############################################################################################
def test_home(client):
    response = client.get("/")
    assert b"<title>Document</title>" in response.data

############################################################################################# Authentication tests ############################################################################################

# test patient:
def test_patient_registration_success(client):
    response = client.post("/PatientRegister", data={
        'username': 'ExistingPatient',
        'id': 'patient1',
        'email': 'newpatient1@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200


    patient = Patient.query.filter_by(user_id='patient1').first()
    assert patient is not None
    assert patient.username == 'ExistingPatient'
    assert patient.email == 'newpatient1@example.com'

def test_patient_registration_failure(client):
    response = client.post("/PatientRegister", data={
        'username': 'ExistingPatient',
        'id': 'patient1',
        'email': 'newpatient1@example.com',
        'password': 'password123'
    })
    assert b"User already exist" in response.data


def test_patient_login_success(client):
    response = client.post("/", data={
        'id': 'patient1',
        'email': 'newpatient1@example.com',
        'password': 'password123',
        'select': 'Patient'
    })
    assert response.status_code == 302

def test_patient_login_failure(client):
    response = client.post("/", data={
        'id': 'patient1',
        'email': 'patient1@example.com',
        'password': 'wrongpassword',
        'select': 'Patient'
    })
    assert b"incorrect field, please log again!" in response.data

# test doctor:
def test_doctor_registration(client):
    response = client.post('/DoctorRegister', data={
        'username': 'test_doctor',
        'id': 'test_doctor_id',
        'email': 'test_doctor@example.com',
        'password': 'test_password',
        'license': 'test_license'
    })
    assert response.status_code == 200

    doctor = Doctor.query.filter_by(user_id='test_doctor_id').first()
    assert doctor is not None
    assert doctor.username == 'test_doctor'
    assert doctor.email == 'test_doctor@example.com'
    assert doctor.doctor_license == 'test_license'


def test_doctor_login_success(client):
    response = client.post("/", data={
        'id': 'test_doctor_id',
        'email': 'test_doctor@example.com',
        'password': 'test_password',
        'select': 'Doctor'
    })
    assert response.status_code == 200

def test_doctor_login_failure(client):
    response = client.post("/", data={
        'id': 'test_doctor_id',
        'email': 'test_doctoree@example.com',
        'password': 'test_passwword',
        'select': 'Doctor'
    })
    assert b"incorrect field, please log again!" in response.data

# manager tests:
manager = Manager(user_id= "manager", username="manager", email="man@gmail.com", password = bcrypt.generate_password_hash("111111").decode('utf-8'))

def test_manager_login_success(client):
    response = client.post("/", data={
        'id': 'manager',
        'email': 'man@gmail.com',
        'password': '111111',
        'select': 'Manager'
    })
    assert response.status_code == 500

def test_manager_login_failure(client):
    response = client.post("/", data={
        'id': 'test_doctor_id',
        'email': 'test_doctoree@example.com',
        'password': 'test_passwword',
        'select': 'Manager'
    })
    assert b"incorrect field, please log again!" in response.data

# test validation functions: 
def test_check_if_patient_exist(client):
    assert check_if_patient_exist('patient1', 'newpatient1@example.com') is True
    assert check_if_patient_exist('nonexistentpatient', 'nonexistent@example.com') is False

def test_check_if_doctor_exist(client):
    assert check_if_doctor_exist('test_doctor_id', 'test_doctor@example.com', 'test_license') is True
    assert check_if_doctor_exist('nonexistentdoctor', 'nonexistent@example.com', 'nonexistentlicense') is False

############################################################################################ Manager Tests ####################################################################################################
# Check if manager approved a doctor successfully.
def test_approve_doctors(app, client):
    with app.test_request_context():
        doctor1 = Doctor.query.filter_by(user_id='test_doctor_id').first()
        
        # Authenticate the manager user
        manager = Manager.query.filter_by(user_id='m').first()
        login_user(manager)

        # Simulate a POST request to the '/approveDoctors' route
        response = client.post('/approveDoctors', data={'doctors': [doctor1.id]})

        # Assert that the response status code is 302 (redirect)
        assert response.status_code == 302

        # Assuming successful approval of doctors, assert that the doctors' 'is_approved' flag is set to True      
        doctor1 = Doctor.query.filter_by(user_id='test_doctor_id').first()

        assert doctor1.is_approved is True

        # Cleanup: Set the 'is_approved' flag back to False for the approved doctors
        doctor1.is_approved = False
        db.session.commit()

# check if all manager reports page is rquested correctly
def test_manager_reports(app, client):
    with app.test_request_context():
        manager = Manager.query.filter_by(user_id='manager').first()
        login_user(manager)
        # Simulate a GET request to the '/ManagerReports' route
        response = client.get('/ManagerReports')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200


# check if all the reports that are not answerd by doctor are correctly loaded to manager.
def test_waiting_for_diagnose(app, client):
    with app.test_request_context():
        # Simulate a GET request to the '/waitingForDiagnose' route
        manager = Manager.query.filter_by(user_id='manager').first()
        login_user(manager)

        response = client.get('/waitingForDiagnose')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

################################################################################## Test Reports ############################################################################
# Test Docotrs Diagnose reports
def test_download_appointment_reports(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the manager user
        manager = Manager.query.filter_by(user_id='manager').first()
        login_user(manager)

        # Simulate a GET request to the '/downloadAppointmentReports' route
        response = client.get('/downloadAppointmentReports')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

        # Assert that the response has the correct content type for a CSV file
        assert response.content_type == 'text/csv' or response.content_type == 'application/vnd.ms-excel'

        # Assert that the response contains the expected attachment filename
        assert 'attachment' in response.headers['Content-Disposition']
        assert response.headers['Content-Disposition'].endswith('AppointmentsReport.csv')

        # Assert that the response content is not empty
        assert response.data


# Test users Login data Manager Report
def test_download_login_reports(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the manager user
        manager = Manager.query.filter_by(user_id='manager').first()
        login_user(manager)

        # Simulate a GET request to the '/downloadLoginReports' route
        response = client.get('/downloadLoginReports')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

        # Assert that the response has the correct content type for a CSV file
        assert response.content_type == 'text/csv' or response.content_type == 'application/vnd.ms-excel'

        # Assert that the response contains the expected attachment filename
        assert 'attachment' in response.headers['Content-Disposition']
        assert response.headers['Content-Disposition'].endswith('UserActivityReport.csv')

        # Assert that the response content is not empty
        assert response.data

# Test users appointment Manager Report
def test_download_appointment_reports(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the manager user
        manager = Manager.query.filter_by(user_id='manager').first()
        login_user(manager)

        # Simulate a GET request to the '/downloadAppointmentReports' route
        response = client.get('/downloadAppointmentReports')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

        # Assert that the response has the correct content type for a CSV file
        assert response.content_type == 'text/csv' or response.content_type == 'application/vnd.ms-excel'

        # Assert that the response contains the expected attachment filename
        assert 'attachment' in response.headers['Content-Disposition']
        assert response.headers['Content-Disposition'].endswith('AppointmentsReport.csv')

        # Assert that the response content is not empty
        assert response.data

################################################################################## Patient tests #########################################################################################################

# Test Patient creating diagnose function
def test_patient_diagnose(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the patient user
        patient = Patient.query.filter_by(user_id='123456789').first()
        login_user(patient)

        # Simulate a GET request to the '/PatientDiagnose' route
        response = client.get('/PatientDiagnose')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

        # Delete test report if it exists
        report = Report.query.order_by(Report.id.desc()).first()
        if report is not None:
            db.session.delete(report)
            db.session.commit()

# Test patient make appointment function
def test_patient_schedule(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the patient user
        patient = Patient.query.filter_by(user_id='123456789').first()
        login_user(patient)

        # Simulate a GET request to the '/PatientScedule' route
        response = client.get('/PatientScedule')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

        # Simulate a POST request to the '/PatientScedule' route
        date_str = '2023-07-05'
        time_str = '10:00'
        doctor_id = 1

        response = client.post('/PatientScedule', data={'date': date_str, 'time': time_str, 'doctor': doctor_id})

        # Assert that the response status code is 200 (success) or 302 (redirect)
        assert response.status_code in [200, 302]

        # Assert that the appointment is created in the database
        appointment = Appointment.query.filter_by(date=datetime.strptime(date_str, '%Y-%m-%d').date(), time=datetime.strptime(time_str, '%H:%M').time(), patient_id=patient.id, doctor_id=doctor_id).first()
        assert appointment is not None

        # Delete the test appointment
        db.session.delete(appointment)
        db.session.commit()

# Test web page - Patient diagnose history
def test_diagnose_history(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the patient user
        patient = Patient.query.filter_by(user_id='123456789').first()
        login_user(patient)

        # Simulate a GET request to the '/DiagnoseHistory' route
        response = client.get('/DiagnoseHistory')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

# Test web page patient reports that not yet answerd
def test_diagnose_report(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the patient user
        patient = Patient.query.filter_by(user_id='123456789').first()
        login_user(patient)

        # Simulate a GET request to the '/DiagnoseReport' route
        response = client.get('/DiagnoseReport')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

##################################################################################### Doctor Tests #####################################################################################################

# Check doctors appointment web page
def test_doctors_appointments(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the doctor user
        doctor = Doctor.query.filter_by(user_id='987654321').first()
        login_user(doctor)

        # Simulate a GET request to the '/DoctorsAppointments' route
        response = client.get('/DoctorsAppointments')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

        # Assert that the appointments are retrieved correctly
        current_date = date.today()
        appointments = Appointment.query.filter(Appointment.doctor_id == '987654321', Appointment.date >= current_date).all()

        # Assert that the rendered appointments match the expected appointments
        rendered_data = response.get_data(as_text=True)
        assert all(str(appointment.id) in rendered_data for appointment in appointments)

# Test Doctor search patient history 
def test_search_patient_history(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the doctor user
        doctor = Doctor.query.filter_by(user_id='987654321').first()
        login_user(doctor)

        # Simulate a GET request to the '/SearchPatientHistory' route
        response = client.get('/SearchPatientHistory')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

        # Simulate a POST request to the '/SearchPatientHistory' route
        response = client.post('/SearchPatientHistory', data={'search': '123456789'})

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

        # Assert that the expected template is rendered based on the patient's existence
        if Patient.query.filter_by(user_id='123456789').first() is not None:
            assert b"Not such Patient" not in response.data
        else:
            assert b"Not such Patient" in response.data

# Test doctor answer web page(rquest help from doctors or answer)
def test_doctor_answer(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the doctor user
        doctor = Doctor.query.filter_by(user_id='987654321').first()
        login_user(doctor)

        # Simulate a GET request to the '/DoctorAnswer' route
        response = client.get('/DoctorAnswer')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

# Test doctor answer page
def test_answer_diagnose(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the doctor user
        doctor = Doctor.query.filter_by(user_id='987654321').first()
        login_user(doctor)

        # Simulate a GET request to the '/AnswerDiagnose' route
        response = client.get('/AnswerDiagnose')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

# Test AI request Help answer function
def test_doctor_ai_help(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the doctor user
        doctor = Doctor.query.filter_by(user_id='987654321').first()
        login_user(doctor)

        # Create a test report
        report = Report(image='test_image.jpeg', patient_id=1, doctor_id=doctor.id)
        db.session.add(report)
        db.session.commit()

        # Simulate a GET request to the '/Doctor_AI_HELP/<report_id>' route
        response = client.get(f'/Doctor_AI_HELP/{report.id}')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

        # Delete the test report
        db.session.delete(report)
        db.session.commit()

# Test Doctor answer after his Diagnose
def test_doctor_answer_details(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the doctor user
        doctor = Doctor.query.filter_by(user_id='987654321').first()
        login_user(doctor)

        # Create a test report
        report = Report(image='test_image.jpeg', patient_id=1, doctor_id=doctor.id)
        db.session.add(report)
        db.session.commit()

        # Simulate a GET request to the '/Doctor_answer-details/<report_id>' route
        response = client.get(f'/Doctor_answer-details/{report.id}')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200


        # Simulate a POST request to the '/Doctor_answer-details/<report_id>' route
        response = client.post(f'/Doctor_answer-details/{report.id}', data={'select': 'Yes'})

        # Assert that the user is redirected to the doctor's home page
        assert response.headers['Location'] == url_for('Authentication.doctorHome')

        # Assert that the report is marked as answered
        updated_report = Report.query.get(report.id)
        assert updated_report.is_answer is True

        # Assert that the report's is_sick property is updated correctly
        assert updated_report.is_sick is True

        # Assert that the report's end_date is updated correctly
        current_date = date.today()
        assert updated_report.end_date == current_date

        # Delete the test report
        db.session.delete(report)
        db.session.commit()


# Test doctor help Diagnose Answer
def test_doctor_help_details(app: Flask, client: FlaskClient):
    with app.test_request_context():
        # Authenticate the doctor user
        doctor = Doctor.query.filter_by(user_id='987654321').first()
        login_user(doctor)

        # Create a test report
        report = Report(image='test_image.jpeg', patient_id=1, doctor_id=doctor.id, helping_doctor_id=doctor.id, is_answer=False, helping_doctor_answer=None)
        db.session.add(report)
        db.session.commit()

        # Simulate a GET request to the '/Doctor_help-details/<report_id>' route
        response = client.get(f'/Doctor_help-details/{report.id}')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200


        # Simulate a POST request to the '/Doctor_help-details/<report_id>' route
        response = client.post(f'/Doctor_help-details/{report.id}', data={'select': 'Yes'})

        # Assert that the user is redirected to the doctor's home page
        assert response.headers['Location'] == url_for('Authentication.doctorHome')

        # Assert that the report's helping_doctor_answer is updated
        updated_report = Report.query.get(report.id)
        assert updated_report.helping_doctor_answer is True

        # Delete the test report
        db.session.delete(report)
        db.session.commit()