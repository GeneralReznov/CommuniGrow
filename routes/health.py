from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
import logging
import uuid
from datetime import datetime, date
from models import HealthService, ChatSession, MentalHealthScreening, SleepWellnessData, TelemedicineSession
from app import db
from gemini import get_health_advice, general_chat_response

health_bp = Blueprint('health', __name__)

@health_bp.route('/')
def index():
    """Health and well-being module main page"""
    emergency_info = {
        'immediate_care': [
            'Call local emergency services: 112 (India national emergency)',
            'Identify nearest hospital or clinic',
            'Keep emergency contacts list updated',
            'Know your medical allergies and conditions',
            'Have basic first aid supplies ready'
        ],
        'preventive_care': [
            'Regular health screenings',
            'Vaccination schedules',
            'Dental care appointments',
            'Eye and hearing checkups',
            'Mental health support'
        ],
        'community_resources': [
            'Free health clinics',
            'Mental health support groups',
            'Nutrition assistance programs',
            'Health education workshops',
            'Community health workers'
        ],
        'warning_signs': {
            'seek_immediate_help': [
                'Severe chest pain',
                'Difficulty breathing',
                'Severe bleeding',
                'Head injury',
                'Thoughts of self-harm'
            ],
            'urgent_care_needed': [
                'High fever',
                'Severe pain',
                'Persistent vomiting',
                'Signs of infection',
                'Medication side effects'
            ]
        }
    }
    
    return render_template('health/index.html', emergency_info=emergency_info)

@health_bp.route('/chatbot')
def chatbot():
    """AI health chatbot interface"""
    return render_template('health/chatbot.html')

@health_bp.route('/services')
def services():
    """Local health services map"""
    return render_template('health/medical_finder.html')

@health_bp.route('/api/health-chat', methods=['POST'])
def health_chat():
    """AI health chatbot endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id', str(uuid.uuid4()))
        chat_type = data.get('type', 'general')  # general, symptoms, mental_health, nutrition
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        if chat_type == 'symptoms':
            # Extract demographic info if provided
            age = data.get('age')
            gender = data.get('gender')
            
            # Get AI health advice
            health_advice = get_health_advice(message, age, gender)
            
            response_text = f"Based on your symptoms, here's my advice:\n\n"
            response_text += f"**Advice:** {health_advice.advice}\n\n"
            response_text += f"**Urgency Level:** {health_advice.urgency_level}\n\n"
            response_text += "**Recommended Actions:**\n"
            for action in health_advice.recommended_actions:
                response_text += f"• {action}\n"
        else:
            # General health chat
            context = f"Health and wellness chat - Type: {chat_type}"
            response_text = general_chat_response(message, context)
        
        # Save chat session
        chat_session = ChatSession()
        chat_session.session_id = session_id
        chat_session.module = 'health'
        chat_session.message = message
        chat_session.response = response_text
        db.session.add(chat_session)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'response': response_text,
            'session_id': session_id
        })
    except Exception as e:
        logging.error(f"Health chat error: {e}")
        return jsonify({
            'success': False,
            'error': 'Health chat service unavailable'
        }), 500

@health_bp.route('/api/health-services')
def get_health_services():
    """Get health services for mapping"""
    try:
        services = HealthService.query.filter_by(is_active=True).all()
        services_data = []
        
        for service in services:
            services_data.append({
                'id': service.id,
                'name': service.name,
                'service_type': service.service_type,
                'address': service.address,
                'latitude': service.latitude,
                'longitude': service.longitude,
                'contact_info': service.contact_info,
                'hours': service.hours,
                'services_offered': service.services_offered
            })
        
        return jsonify({
            'success': True,
            'services': services_data
        })
    except Exception as e:
        logging.error(f"Health services error: {e}")
        return jsonify({
            'success': False,
            'error': 'Unable to load health services'
        }), 500

@health_bp.route('/api/nearby-facilities')
def get_nearby_facilities():
    """Get nearby medical facilities for mapping with location filtering"""
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', type=float, default=5)  # km
        facility_type = request.args.get('type', default='all')
        
        # Start with base query
        query = HealthService.query.filter_by(is_active=True)
        
        # Filter by facility type if specified
        if facility_type and facility_type != 'all':
            query = query.filter(HealthService.service_type.ilike(f'%{facility_type}%'))
        
        services = query.all()
        facilities_data = []
        
        # Convert services to the expected format for the map
        for service in services:
            # Skip if no location data
            if not service.latitude or not service.longitude:
                continue
                
            # Calculate distance if lat/lng provided (basic calculation)
            if lat and lng:
                # Simple distance calculation - for production use haversine formula
                lat_diff = abs(service.latitude - lat)
                lng_diff = abs(service.longitude - lng)
                distance = ((lat_diff ** 2) + (lng_diff ** 2)) ** 0.5 * 111  # Rough km conversion
                
                # Skip if outside radius
                if distance > radius:
                    continue
            
            # Format phone number
            phone = service.contact_info if service.contact_info else 'Not available'
            
            facilities_data.append({
                'id': service.id,
                'name': service.name,
                'type': service.service_type.lower(),
                'address': service.address,
                'lat': service.latitude,
                'lng': service.longitude,
                'phone': phone,
                'hours': service.hours if service.hours else 'Hours not available',
                'services': service.services_offered if service.services_offered else 'General medical services'
            })
        
        return jsonify({
            'success': True,
            'facilities': facilities_data
        })
    except Exception as e:
        logging.error(f"Nearby facilities error: {e}")
        return jsonify({
            'success': False,
            'error': 'Unable to load nearby facilities'
        }), 500

@health_bp.route('/self-assessment')
def self_assessment():
    """Health self-assessment tools"""
    assessments = {
        'mental_health': {
            'title': 'Mental Health Check',
            'questions': [
                'How often have you felt down, depressed, or hopeless in the past 2 weeks?',
                'How often have you had little interest or pleasure in doing things?',
                'How would you rate your stress level?',
                'How well are you sleeping?',
                'How is your appetite?'
            ],
            'scoring': 'Each question scored 0-3, total score indicates severity'
        },
        'physical_health': {
            'title': 'Physical Health Check',
            'questions': [
                'How often do you exercise per week?',
                'How would you rate your energy level?',
                'Do you experience regular pain or discomfort?',
                'How is your mobility and balance?',
                'When was your last health checkup?'
            ],
            'scoring': 'Identifies areas needing attention'
        },
        'nutrition': {
            'title': 'Nutrition Assessment',
            'questions': [
                'How many servings of fruits and vegetables do you eat daily?',
                'How often do you eat processed foods?',
                'How much water do you drink daily?',
                'Do you take any vitamins or supplements?',
                'How regular are your meal times?'
            ],
            'scoring': 'Evaluates nutritional habits and needs'
        }
    }
    
    return render_template('health/index.html', assessments=assessments)

@health_bp.route('/emergency-info')
def emergency_info():
    """Emergency health information and contacts"""
    emergency_info = {
        'immediate_care': [
            'Call local emergency services: 911 or local equivalent',
            'Identify nearest hospital or clinic',
            'Keep emergency contacts list updated',
            'Know your medical allergies and conditions',
            'Have basic first aid supplies ready'
        ],
        'preventive_care': [
            'Regular health screenings',
            'Vaccination schedules',
            'Dental care appointments',
            'Eye and hearing checkups',
            'Mental health support'
        ],
        'community_resources': [
            'Free health clinics',
            'Mental health support groups',
            'Nutrition assistance programs',
            'Health education workshops',
            'Community health workers'
        ],
        'warning_signs': {
            'seek_immediate_help': [
                'Severe chest pain',
                'Difficulty breathing',
                'Severe bleeding',
                'Head injury',
                'Thoughts of self-harm'
            ],
            'urgent_care_needed': [
                'High fever',
                'Severe pain',
                'Persistent vomiting',
                'Signs of infection',
                'Medication side effects'
            ]
        }
    }
    
    return render_template('health/index.html', emergency_info=emergency_info)

@health_bp.route('/maternal-health')
def maternal_health():
    """Maternal and child health resources"""
    maternal_resources = {
        'prenatal_care': [
            'Regular checkups schedule',
            'Nutrition during pregnancy',
            'Exercise and activity guidelines',
            'Warning signs to watch for',
            'Preparation for childbirth'
        ],
        'postnatal_care': [
            'Newborn care basics',
            'Breastfeeding support',
            'Postpartum mental health',
            'Family planning resources',
            'Child development milestones'
        ],
        'child_health': [
            'Vaccination schedules',
            'Nutrition for children',
            'Growth monitoring',
            'Common childhood illnesses',
            'Educational development support'
        ]
    }
    
    return render_template('health/index.html', maternal_resources=maternal_resources)

# Mental Health Screening Routes
@health_bp.route('/mental-health')
def mental_health():
    """Mental health screening hub"""
    return render_template('health/mental_health.html')

@health_bp.route('/depression-screening')
def depression_screening():
    """Depression screening form (PHQ-9)"""
    return render_template('health/depression_screening.html')

@health_bp.route('/anxiety-screening')
def anxiety_screening():
    """Anxiety screening form (GAD-7)"""
    return render_template('health/anxiety_screening.html')

@health_bp.route('/stress-screening')
def stress_screening():
    """Stress screening form (PSS-10)"""
    return render_template('health/stress_screening.html')

@health_bp.route('/process-mental-health-screening', methods=['POST'])
def process_mental_health_screening():
    """Process mental health screening results"""
    try:
        screening_type = request.form.get('screening_type')
        additional_notes = request.form.get('additional_notes', '')
        
        # Calculate score based on screening type
        if screening_type == 'depression':
            score = sum(int(request.form.get(f'q{i}', 0)) for i in range(1, 10))
            if score <= 4:
                risk_level = 'low'
                recommendations = 'Minimal depression symptoms. Continue monitoring your mood and maintain healthy habits.'
            elif score <= 9:
                risk_level = 'moderate'
                recommendations = 'Mild depression symptoms. Consider speaking with a healthcare professional or counselor.'
            elif score <= 14:
                risk_level = 'moderate'
                recommendations = 'Moderate depression symptoms. We recommend consulting with a mental health professional.'
            else:
                risk_level = 'high'
                recommendations = 'Severe depression symptoms. Please seek immediate professional help. Contact a healthcare provider or call 988 for crisis support.'
        
        elif screening_type == 'anxiety':
            score = sum(int(request.form.get(f'q{i}', 0)) for i in range(1, 8))
            if score <= 4:
                risk_level = 'low'
                recommendations = 'Minimal anxiety symptoms. Practice stress management techniques and maintain healthy routines.'
            elif score <= 9:
                risk_level = 'moderate'
                recommendations = 'Mild anxiety symptoms. Consider relaxation techniques, exercise, or speaking with a counselor.'
            elif score <= 14:
                risk_level = 'moderate'
                recommendations = 'Moderate anxiety symptoms. We recommend professional consultation and anxiety management strategies.'
            else:
                risk_level = 'high'
                recommendations = 'Severe anxiety symptoms. Please seek professional help. Contact a healthcare provider for anxiety treatment options.'
        
        elif screening_type == 'stress':
            score = sum(int(request.form.get(f'q{i}', 0)) for i in range(1, 6))
            if score <= 6:
                risk_level = 'low'
                recommendations = 'Low stress levels. Continue current stress management practices and maintain work-life balance.'
            elif score <= 12:
                risk_level = 'moderate'
                recommendations = 'Moderate stress levels. Consider stress reduction techniques, time management, and relaxation practices.'
            else:
                risk_level = 'high'
                recommendations = 'High stress levels. We recommend professional stress management counseling and lifestyle changes.'
        
        # Save screening results
        screening = MentalHealthScreening()
        screening.screening_type = screening_type
        screening.score = score
        screening.risk_level = risk_level
        screening.recommendations = recommendations
        screening.additional_notes = additional_notes
        screening.session_id = str(uuid.uuid4())
        
        db.session.add(screening)
        db.session.commit()
        
        # Generate AI recommendations
        ai_recommendations = generate_ai_mental_health_recommendations(screening_type, score, risk_level)
        
        return render_template('health/mental_health_results.html', 
                             screening=screening, 
                             ai_recommendations=ai_recommendations)
    
    except Exception as e:
        logging.error(f"Error processing mental health screening: {e}")
        flash('There was an error processing your assessment. Please try again.', 'error')
        return redirect(url_for('health.mental_health'))

# Sleep Wellness Routes
@health_bp.route('/sleep-wellness')
def sleep_wellness():
    """Sleep wellness tracking form"""
    return render_template('health/sleep_wellness.html')

@health_bp.route('/track-sleep-wellness', methods=['POST'])
def track_sleep_wellness():
    """Process sleep wellness data"""
    try:
        # Get form data
        sleep_date_str = request.form.get('sleep_date')
        sleep_duration_str = request.form.get('sleep_duration')
        sleep_quality_str = request.form.get('sleep_quality')
        fatigue_level_str = request.form.get('fatigue_level')
        alertness_level_str = request.form.get('alertness_level')
        
        # Validate required fields
        if not all([sleep_date_str, sleep_duration_str, sleep_quality_str, fatigue_level_str, alertness_level_str]):
            raise ValueError("All fields are required")
            
        sleep_duration = float(sleep_duration_str)
        sleep_quality = int(sleep_quality_str)
        fatigue_level = int(fatigue_level_str)
        alertness_level = int(alertness_level_str)
        notes = request.form.get('notes', '')
        
        # Convert date string to date object
        if not sleep_date_str:
            raise ValueError("Sleep date is required")
        sleep_date = datetime.strptime(sleep_date_str, '%Y-%m-%d').date()
        
        # Calculate wellness score (0-100)
        # Formula: Consider sleep duration (optimal 7-9h), quality, fatigue (inverted), alertness
        duration_score = min(100, max(0, 100 - abs(sleep_duration - 8) * 12.5))  # Optimal at 8 hours
        quality_score = sleep_quality * 10
        fatigue_score = (11 - fatigue_level) * 10  # Invert fatigue (lower is better)
        alertness_score = alertness_level * 10
        
        wellness_score = int((duration_score + quality_score + fatigue_score + alertness_score) / 4)
        
        # Save sleep data
        sleep_data = SleepWellnessData()
        sleep_data.sleep_date = sleep_date
        sleep_data.sleep_duration = sleep_duration
        sleep_data.sleep_quality = sleep_quality
        sleep_data.fatigue_level = fatigue_level
        sleep_data.alertness_level = alertness_level
        sleep_data.notes = notes
        sleep_data.wellness_score = wellness_score
        sleep_data.session_id = str(uuid.uuid4())
        
        db.session.add(sleep_data)
        db.session.commit()
        
        # Generate AI insights
        insights = generate_sleep_insights(sleep_data)
        
        return render_template('health/sleep_insights.html', 
                             sleep_data=sleep_data, 
                             insights=insights)
    
    except Exception as e:
        logging.error(f"Error tracking sleep wellness: {e}")
        flash('There was an error saving your sleep data. Please try again.', 'error')
        return redirect(url_for('health.sleep_wellness'))

# Telemedicine Routes
@health_bp.route('/telemedicine')
def telemedicine():
    """Telemedicine and support interface"""
    # Get recent telemedicine sessions
    telemedicine_sessions = TelemedicineSession.query.order_by(TelemedicineSession.created_at.desc()).limit(5).all()
    return render_template('health/telemedicine.html', telemedicine_sessions=telemedicine_sessions)

@health_bp.route('/schedule-consultation', methods=['POST'])
def schedule_consultation():
    """Schedule a telemedicine consultation"""
    try:
        consultation_type = request.form.get('consultation_type')
        preferred_date = request.form.get('preferred_date')
        preferred_time = request.form.get('preferred_time')
        consultation_notes = request.form.get('consultation_notes', '')
        contact_preference = request.form.get('contact_preference')
        
        # Parse scheduled time
        scheduled_time = None
        if preferred_date:
            scheduled_time = datetime.strptime(preferred_date, '%Y-%m-%d')
        
        # Create telemedicine session
        session = TelemedicineSession()
        session.session_type = 'consultation'
        session.status = 'scheduled'
        session.session_notes = f"Type: {consultation_type}\nTime preference: {preferred_time}\nContact: {contact_preference}\nNotes: {consultation_notes}"
        session.priority_level = 'normal'
        session.scheduled_time = scheduled_time
        session.session_id = str(uuid.uuid4())
        
        db.session.add(session)
        db.session.commit()
        
        flash('Your consultation has been scheduled! We will contact you soon to confirm the details.', 'success')
        return redirect(url_for('health.telemedicine'))
    
    except Exception as e:
        logging.error(f"Error scheduling consultation: {e}")
        flash('There was an error scheduling your consultation. Please try again.', 'error')
        return redirect(url_for('health.telemedicine'))

# Helper functions
def generate_ai_mental_health_recommendations(screening_type, score, risk_level):
    """Generate AI-powered mental health recommendations"""
    try:
        context = f"Mental health {screening_type} screening with score {score} and {risk_level} risk level"
        prompt = f"Provide 3-5 specific, actionable recommendations for someone with {screening_type} screening results showing {risk_level} risk (score: {score}). Focus on practical self-care strategies, when to seek professional help, and community resources."
        
        response = general_chat_response(prompt, context)
        
        # Split response into bullet points
        recommendations = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                recommendations.append(line.lstrip('•-* '))
            elif line and len(line) > 20:  # Likely a recommendation sentence
                recommendations.append(line)
        
        # Fallback recommendations if AI fails
        if not recommendations:
            if screening_type == 'depression':
                recommendations = [
                    "Maintain a regular sleep schedule and aim for 7-9 hours of sleep",
                    "Engage in regular physical activity, even light walking can help",
                    "Connect with friends, family, or support groups",
                    "Practice mindfulness or meditation techniques",
                    "Consider professional counseling if symptoms persist"
                ]
            elif screening_type == 'anxiety':
                recommendations = [
                    "Practice deep breathing exercises when feeling anxious",
                    "Try progressive muscle relaxation techniques",
                    "Limit caffeine intake, especially in the afternoon",
                    "Establish a calming bedtime routine",
                    "Consider cognitive behavioral therapy (CBT) techniques"
                ]
            else:  # stress
                recommendations = [
                    "Identify and address sources of stress in your life",
                    "Practice time management and prioritization skills",
                    "Take regular breaks throughout your day",
                    "Engage in stress-reducing activities like yoga or meditation",
                    "Build a strong support network of friends and family"
                ]
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    except Exception as e:
        logging.error(f"Error generating AI recommendations: {e}")
        return ["Consider speaking with a healthcare professional for personalized guidance"]

def generate_sleep_insights(sleep_data):
    """Generate AI-powered sleep insights"""
    try:
        prompt = f"Analyze this sleep data and provide 3-4 insights and recommendations: Duration: {sleep_data.sleep_duration}h, Quality: {sleep_data.sleep_quality}/10, Fatigue: {sleep_data.fatigue_level}/10, Alertness: {sleep_data.alertness_level}/10, Wellness Score: {sleep_data.wellness_score}/100"
        
        response = general_chat_response(prompt, "Sleep wellness analysis")
        
        # Split response into insights
        insights = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                insights.append(line.lstrip('•-* '))
            elif line and len(line) > 20:
                insights.append(line)
        
        # Fallback insights
        if not insights:
            if sleep_data.wellness_score >= 80:
                insights = [
                    "Excellent sleep patterns! Your wellness score indicates healthy sleep habits.",
                    "Continue maintaining your current sleep schedule and bedtime routine.",
                    "Your sleep quality and duration are well-balanced for optimal health."
                ]
            elif sleep_data.wellness_score >= 60:
                insights = [
                    "Good sleep patterns with room for improvement.",
                    "Consider optimizing your sleep environment for better quality rest.",
                    "Try to maintain consistent sleep and wake times every day."
                ]
            else:
                insights = [
                    "Your sleep patterns show signs that could benefit from attention.",
                    "Consider establishing a regular bedtime routine and sleep schedule.",
                    "Limit screen time before bed and create a calm sleep environment.",
                    "If sleep issues persist, consider consulting with a healthcare provider."
                ]
        
        return insights[:4]  # Limit to 4 insights
    
    except Exception as e:
        logging.error(f"Error generating sleep insights: {e}")
        return ["Track your sleep consistently to identify patterns and improve your rest quality."]
