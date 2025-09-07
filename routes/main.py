from flask import Blueprint, render_template, request, jsonify
import logging

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Landing page with mission statement and voice tour"""
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """Main dashboard with 4 core feature modules"""
    return render_template('dashboard.html')

@main_bp.route('/voice-tour')
def voice_tour():
    """Voice-guided tour of the platform"""
    return render_template('dashboard.html', voice_tour=True)

@main_bp.route('/api/voice/speak', methods=['POST'])
def text_to_speech():
    """API endpoint for text-to-speech conversion"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        # Return text for client-side TTS
        return jsonify({
            'success': True,
            'text': text,
            'message': 'Text ready for speech synthesis'
        })
    except Exception as e:
        logging.error(f"TTS error: {e}")
        return jsonify({
            'success': False,
            'error': 'Speech synthesis failed'
        }), 500

@main_bp.route('/api/voice/listen', methods=['POST'])
def speech_to_text():
    """API endpoint for speech-to-text conversion"""
    try:
        # This would typically handle audio data
        # For now, return success for client-side STT
        return jsonify({
            'success': True,
            'message': 'Ready to listen'
        })
    except Exception as e:
        logging.error(f"STT error: {e}")
        return jsonify({
            'success': False,
            'error': 'Speech recognition failed'
        }), 500
