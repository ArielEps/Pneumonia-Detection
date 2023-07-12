# Pneumonia Detection System

This project aims to assist doctors in diagnosing pneumonia by analyzing chest X-rays. The system utilizes machine learning techniques to analyze the images and provide diagnostic predictions. It provides a user-friendly interface for patients, doctors, and managers to interact with the system efficiently.

## Installation

To install and run the Pneumonia Detection System, follow these steps:

1. Ensure Python is installed on your computer. You can download the latest version of Python from the official Python website (https://www.python.org) and follow the installation instructions specific to your operating system.

2. Set up a virtual environment by running the following command in your command prompt or terminal:
 
  ```
  python -m venv venv
  ```

3. Activate the virtual environment:

- For Windows:

  ```
  .\venv\Scripts\activate
  ```

- For macOS/Linux:

  ```
  source venv/bin/activate
  ```

4. Clone the project repository from GitHub:
  ```
 git clone https://github.com/ArielEps/Pneumonia-Detection.git
  ```

5. Navigate to the project directory:

  ```
  cd Pneumonia-Detection
  ```

6. Install the required libraries:
  ```
  pip install -r requirements.txt
  ```

7. Run the software:
  ```
  python run.py
  ```

## Functionality

### Patient

- Registration and connection to the system.
- Uploading an X-ray image and choosing a diagnostician for the purpose of receiving a diagnosis.
- Receiving a list of diagnoses awaiting diagnosis from a doctor.
- Making appointments with a doctor after receiving the diagnosis result for continued treatment.
- Accessing the history of treatments and diagnoses.
- Password change.

### Manager

- Approving doctors who register in the system (license check).
- Receiving information on patients who have not received diagnostic results, including the date of diagnosis, patient details, and doctor details.
- Generating reports on system activity, doctor diagnoses, and doctors' meetings with patients.
- Password change.

### Doctor

- Registration to the system with license and medical certificate verification.
- Generating diagnostic reports.
- Cooperating and consulting with other doctors.
- Accessing a patient's medical history.
- Requesting help from an AI system to identify diseases.
- Viewing the schedule of upcoming appointments.

Please refer to the project's documentation for detailed instructions on how to use each functionality.

### Video:

https://youtu.be/uA9o92FAEuw

## License

[MIT License](LICENSE)
