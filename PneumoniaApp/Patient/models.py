from PneumoniaApp import db
from datetime import datetime

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120), unique=True, nullable=False)
    
    start_date = db.Column(db.Date, default=datetime.utcnow)
    end_date = db.Column(db.Date)
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    
    helping_doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    helping_doctor_answer = db.Column(db.Boolean)
    
    ai_help = db.Column(db.Boolean, default=False)
    ai_answer = db.Column(db.Boolean)
    
    is_sick = db.Column(db.Boolean)
    is_answer=db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Report('{self.image}', '{self.patient_id}', '{self.doctor_id}')"