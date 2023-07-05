from PneumoniaApp.Authentication.models import *
from PneumoniaApp.Authentication.routes import bcrypt
from PneumoniaApp.Authentication.validate import *
from flask_login import login_user
from flask import url_for
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