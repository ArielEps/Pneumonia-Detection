from PneumoniaApp.Authentication.models import *
from PneumoniaApp.Authentication.routes import bcrypt
from PneumoniaApp.Authentication.validate import *
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
    assert response.status_code == 200

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
