from app import db
from datetime import datetime

class WeatherAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

class SkillListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skill_category = db.Column(db.String(100), nullable=False)
    difficulty_level = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))
    is_remote = db.Column(db.Boolean, default=False)
    contact_info = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JobListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    is_remote = db.Column(db.Boolean, default=False)
    skills_required = db.Column(db.Text)
    salary_range = db.Column(db.String(100))
    contact_info = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FoodListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)  # 'marketplace', 'sharing', 'surplus'
    price = db.Column(db.Float)
    quantity = db.Column(db.String(100))
    location = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(200))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class HealthService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    contact_info = db.Column(db.String(200))
    hours = db.Column(db.String(200))
    services_offered = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    module = db.Column(db.String(50), nullable=False)  # 'health', 'nutrition', 'mental_health'
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MentalHealthScreening(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    screening_type = db.Column(db.String(50), nullable=False)  # 'depression', 'anxiety', 'stress'
    score = db.Column(db.Integer, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)  # 'low', 'moderate', 'high'
    recommendations = db.Column(db.Text)
    additional_notes = db.Column(db.Text)
    session_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SleepWellnessData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sleep_date = db.Column(db.Date, nullable=False)
    sleep_duration = db.Column(db.Float, nullable=False)  # hours
    sleep_quality = db.Column(db.Integer, nullable=False)  # 1-10 scale
    fatigue_level = db.Column(db.Integer, nullable=False)  # 1-10 scale
    alertness_level = db.Column(db.Integer, nullable=False)  # 1-10 scale
    notes = db.Column(db.Text)
    wellness_score = db.Column(db.Integer)  # calculated score 0-100
    session_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TelemedicineSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_type = db.Column(db.String(50), nullable=False)  # 'ai_chat', 'emergency', 'consultation'
    status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'scheduled'
    provider_name = db.Column(db.String(200))
    session_notes = db.Column(db.Text)
    priority_level = db.Column(db.String(20), default='normal')  # 'low', 'normal', 'high', 'emergency'
    contact_info = db.Column(db.String(200))
    scheduled_time = db.Column(db.DateTime)
    session_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DisasterPreparednessAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))
    disaster_type = db.Column(db.String(50), nullable=False)  # 'flood', 'hurricane', 'earthquake', 'drought'
    preparedness_score = db.Column(db.Integer)
    recommendations = db.Column(db.Text)
    risk_level = db.Column(db.String(20))  # 'low', 'medium', 'high'
    location = db.Column(db.String(100))
    responses = db.Column(db.Text)  # JSON string of question responses
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
