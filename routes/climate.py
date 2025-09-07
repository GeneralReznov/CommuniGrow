from flask import Blueprint, render_template, request, jsonify
import requests
import os
import logging
from models import WeatherAlert, DisasterPreparednessAssessment
from app import db
from gemini import get_climate_advice, get_india_weather, assess_disaster_preparedness
import json

climate_bp = Blueprint('climate', __name__)

@climate_bp.route('/')
def index():
    """Climate action module main page"""
    return render_template('climate/index.html')

@climate_bp.route('/alerts')
def alerts():
    """Climate and disaster risk alerts"""
    active_alerts = WeatherAlert.query.filter_by(is_active=True).order_by(WeatherAlert.created_at.desc()).all()
    return render_template('climate/alerts.html', alerts=active_alerts)

@climate_bp.route('/api/weather/<location>')
def get_weather(location):
    """Get weather data for India using Gemini AI"""
    try:
        # Use Gemini API to get India weather data
        india_location = f"{location}" if "india" in location.lower() else f"{location}, India"
        weather_advice = get_india_weather(india_location)
        
        return jsonify({
            'success': True,
            'weather': {
                'location': india_location,
                'conditions': weather_advice.current_conditions,
                'temperature': weather_advice.temperature,
                'humidity': weather_advice.humidity
            },
            'advice': weather_advice.recommendations,
            'warnings': weather_advice.warnings
        })
    except Exception as e:
        logging.error(f"Weather API error: {e}")
        return jsonify({
            'success': False,
            'error': 'Unable to fetch weather data for India'
        }), 500

@climate_bp.route('/api/alerts', methods=['POST'])
def create_alert():
    """Create a new weather alert"""
    try:
        data = request.get_json()
        
        alert = WeatherAlert(
            location=data.get('location', ''),
            alert_type=data.get('alert_type', ''),
            severity=data.get('severity', ''),
            message=data.get('message', ''),
            expires_at=data.get('expires_at')
        )
        
        db.session.add(alert)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Alert created successfully'
        })
    except Exception as e:
        logging.error(f"Alert creation error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to create alert'
        }), 500

@climate_bp.route('/sustainable-practices')
def sustainable_practices():
    """Sustainable farming and energy practices"""
    practices = {
        'farming': [
            'Crop rotation to maintain soil health',
            'Rainwater harvesting systems',
            'Composting organic waste',
            'Drought-resistant crop varieties',
            'Natural pest control methods'
        ],
        'energy': [
            'Solar panel installation basics',
            'Energy-efficient cooking methods',
            'LED lighting conversion',
            'Insulation improvements',
            'Smart energy usage timing'
        ],
        'water': [
            'Greywater recycling systems',
            'Drip irrigation techniques',
            'Water conservation practices',
            'Rainwater collection methods',
            'Well water protection'
        ]
    }
    
    return render_template('climate/index.html', practices=practices)

@climate_bp.route('/disaster-assessment')
def disaster_assessment():
    """Disaster preparedness assessment page"""
    return render_template('climate/disaster_assessment.html')

@climate_bp.route('/climate-monitoring')
def climate_monitoring():
    """Climate monitoring page with India heatmap and forecast"""
    return render_template('climate/climate_monitoring.html')

@climate_bp.route('/api/disaster-assessment', methods=['POST'])
def submit_disaster_assessment():
    """Submit disaster preparedness assessment"""
    try:
        data = request.get_json()
        disaster_type = data.get('disaster_type', 'general')
        responses = data.get('responses', {})
        location = data.get('location', 'India')
        session_id = data.get('session_id', 'default')
        
        # Get AI assessment
        assessment = assess_disaster_preparedness(disaster_type, responses, location)
        
        # Save to database
        db_assessment = DisasterPreparednessAssessment(
            session_id=session_id,
            disaster_type=disaster_type,
            preparedness_score=assessment.preparedness_score,
            recommendations=json.dumps(assessment.recommendations),
            risk_level=assessment.risk_level,
            location=location,
            responses=json.dumps(responses)
        )
        
        db.session.add(db_assessment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'assessment': {
                'score': assessment.preparedness_score,
                'risk_level': assessment.risk_level,
                'recommendations': assessment.recommendations,
                'immediate_actions': assessment.immediate_actions,
                'supplies_needed': assessment.supplies_needed
            }
        })
        
    except Exception as e:
        logging.error(f"Disaster assessment error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to process assessment'
        }), 500

@climate_bp.route('/api/iot-sensors')
def iot_sensors():
    """Get IoT sensor data if hardware is detected"""
    try:
        # Check for IoT hardware (placeholder - would detect actual hardware)
        sensors_detected = False  # Replace with actual hardware detection
        
        if sensors_detected:
            # Return actual sensor data
            sensor_data = {
                'air_quality': {'aqi': 45, 'status': 'Good'},
                'water_quality': {'ph': 7.2, 'turbidity': 'Low'},
                'solar_energy': {'output': '2.5kW', 'efficiency': '85%'}
            }
        else:
            sensor_data = {
                'message': 'No IoT sensors detected. Connect compatible hardware to view environmental data.'
            }
        
        return jsonify({
            'success': True,
            'sensors_detected': sensors_detected,
            'data': sensor_data
        })
    except Exception as e:
        logging.error(f"IoT sensor error: {e}")
        return jsonify({
            'success': False,
            'error': 'Sensor data unavailable'
        }), 500
