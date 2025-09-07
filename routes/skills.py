from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import logging
import uuid
from datetime import datetime
from models import SkillListing, JobListing
from app import db
from gemini import match_job_to_skills, general_chat_response

skills_bp = Blueprint('skills', __name__)

@skills_bp.route('/')
def index():
    """Skills and employment module main page"""
    recent_jobs = JobListing.query.order_by(JobListing.created_at.desc()).limit(5).all()
    recent_skills = SkillListing.query.order_by(SkillListing.created_at.desc()).limit(5).all()
    
    return render_template('skills/index.html', recent_jobs=recent_jobs, recent_skills=recent_skills)

@skills_bp.route('/jobs')
def jobs():
    """Job listings and matching"""
    all_jobs = JobListing.query.order_by(JobListing.created_at.desc()).all()
    return render_template('skills/jobs.html', jobs=all_jobs)

@skills_bp.route('/learning')
def learning():
    """Microlearning and skill development"""
    learning_modules = {
        'digital_literacy': {
            'title': 'Digital Literacy Basics',
            'lessons': [
                'Computer fundamentals',
                'Internet safety',
                'Email communication',
                'Online job applications',
                'Digital banking basics'
            ]
        },
        'entrepreneurship': {
            'title': 'Small Business Development',
            'lessons': [
                'Business plan creation',
                'Financial management',
                'Marketing strategies',
                'Customer service',
                'Legal requirements'
            ]
        },
        'technical_skills': {
            'title': 'Technical Skills Training',
            'lessons': [
                'Basic computer repair',
                'Mobile phone services',
                'Agricultural technology',
                'Renewable energy basics',
                'Water system maintenance'
            ]
        },
        'life_skills': {
            'title': 'Life Skills Development',
            'lessons': [
                'Communication skills',
                'Time management',
                'Problem solving',
                'Leadership development',
                'Conflict resolution'
            ]
        }
    }
    
    return render_template('skills/learning.html', modules=learning_modules)

@skills_bp.route('/case-prep')
def case_prep():
    """Career development planning with AI assistance"""
    return render_template('skills/case_prep.html')

@skills_bp.route('/tutorials')
def tutorials():
    """Skills tutorials and interactive learning"""
    return render_template('skills/tutorials.html')

@skills_bp.route('/api/job-match', methods=['POST'])
def job_match():
    """AI-powered job matching"""
    try:
        data = request.get_json()
        job_description = data.get('job_description', '')
        user_skills = data.get('skills', [])
        
        if not job_description or not user_skills:
            return jsonify({
                'success': False,
                'error': 'Job description and skills are required'
            }), 400
        
        # Use Gemini AI for job matching
        match_result = match_job_to_skills(job_description, user_skills)
        
        return jsonify({
            'success': True,
            'match_score': match_result.match_score,
            'reasons': match_result.reasons,
            'skill_gaps': match_result.skill_gaps,
            'recommendations': match_result.recommendations
        })
    except Exception as e:
        logging.error(f"Job matching error: {e}")
        return jsonify({
            'success': False,
            'error': 'Job matching service unavailable'
        }), 500

@skills_bp.route('/post-job', methods=['GET', 'POST'])
def post_job():
    """Post a new job listing"""
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            
            job = JobListing(
                title=data.get('title'),
                description=data.get('description'),
                company=data.get('company'),
                location=data.get('location'),
                is_remote=data.get('is_remote', False),
                skills_required=data.get('skills_required'),
                salary_range=data.get('salary_range'),
                contact_info=data.get('contact_info')
            )
            
            db.session.add(job)
            db.session.commit()
            
            if request.is_json:
                return jsonify({
                    'success': True,
                    'message': 'Job posted successfully'
                })
            else:
                return redirect(url_for('skills.jobs'))
        except Exception as e:
            logging.error(f"Job posting error: {e}")
            if request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Failed to post job'
                }), 500
            else:
                return render_template('skills/jobs.html', error='Failed to post job')
    
    return render_template('skills/jobs.html', show_form=True)

@skills_bp.route('/post-skill', methods=['GET', 'POST'])
def post_skill():
    """Post a new skill offering"""
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            
            skill = SkillListing(
                title=data.get('title'),
                description=data.get('description'),
                skill_category=data.get('skill_category'),
                difficulty_level=data.get('difficulty_level'),
                location=data.get('location'),
                is_remote=data.get('is_remote', False),
                contact_info=data.get('contact_info')
            )
            
            db.session.add(skill)
            db.session.commit()
            
            if request.is_json:
                return jsonify({
                    'success': True,
                    'message': 'Skill posted successfully'
                })
            else:
                return redirect(url_for('skills.index'))
        except Exception as e:
            logging.error(f"Skill posting error: {e}")
            if request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Failed to post skill'
                }), 500
            else:
                return render_template('skills/index.html', error='Failed to post skill')
    
    return render_template('skills/index.html', show_skill_form=True)

@skills_bp.route('/volunteer-opportunities')
def volunteer_opportunities():
    """Community volunteer opportunities"""
    opportunities = [
        {
            'title': 'Community Garden Coordinator',
            'description': 'Help manage local community gardens and teach sustainable farming',
            'time_commitment': '4 hours/week',
            'skills_gained': ['Leadership', 'Agriculture', 'Community organizing']
        },
        {
            'title': 'Digital Literacy Instructor',
            'description': 'Teach basic computer and internet skills to community members',
            'time_commitment': '3 hours/week',
            'skills_gained': ['Teaching', 'Technology', 'Communication']
        },
        {
            'title': 'Health Education Advocate',
            'description': 'Provide health education and connect people with healthcare resources',
            'time_commitment': '5 hours/week',
            'skills_gained': ['Public health', 'Communication', 'Research']
        },
        {
            'title': 'Youth Mentorship Program',
            'description': 'Mentor young adults in career development and life skills',
            'time_commitment': '2 hours/week',
            'skills_gained': ['Mentoring', 'Career guidance', 'Youth development']
        }
    ]
    
    return render_template('skills/index.html', volunteer_opportunities=opportunities)

@skills_bp.route('/api/career-plan', methods=['POST'])
def generate_career_plan():
    """Generate AI-powered career development plan"""
    try:
        data = request.form
        career_goal = data.get('careerGoal', '')
        current_level = data.get('currentLevel', '')
        timeframe = data.get('timeframe', '')
        current_skills = data.get('currentSkills', '')
        
        if not career_goal or not current_level:
            return jsonify({
                'success': False,
                'error': 'Career goal and current level are required'
            }), 400
        
        # Create prompt for AI career planning
        prompt = f"""
        Create a comprehensive career development plan for someone with the following details:
        
        Career Goal: {career_goal}
        Current Level: {current_level}
        Timeline: {timeframe}
        Current Skills: {current_skills}
        
        Please provide:
        1. A clear learning pathway with specific steps
        2. Skill development priorities
        3. Resources and opportunities to pursue
        4. Realistic milestones and timelines
        5. Potential challenges and how to overcome them
        
        Focus on practical, actionable advice for someone in an underserved community.
        """
        
        # Get AI response
        ai_response = general_chat_response(prompt, "Career development planning")
        
        return jsonify({
            'success': True,
            'plan': {
                'full_text': ai_response
            }
        })
        
    except Exception as e:
        logging.error(f"Career planning error: {e}")
        return jsonify({
            'success': False,
            'error': 'Career planning service unavailable'
        }), 500

@skills_bp.route('/api/skill-assessment', methods=['POST'])
def skill_assessment():
    """AI-powered skill assessment"""
    try:
        data = request.get_json()
        responses = data.get('responses', {})
        skill_area = data.get('skill_area', 'general')
        
        if not responses:
            return jsonify({
                'success': False,
                'error': 'Assessment responses are required'
            }), 400
        
        # Create assessment prompt
        prompt = f"""
        Assess the skill level and provide recommendations based on these assessment responses:
        
        Skill Area: {skill_area}
        Responses: {responses}
        
        Please provide:
        1. Current skill level (Beginner/Intermediate/Advanced)
        2. Specific strengths identified
        3. Areas for improvement
        4. Recommended learning path
        5. Suggested next steps
        
        Focus on practical, community-relevant skills development.
        """
        
        ai_response = general_chat_response(prompt, "Skill assessment")
        
        return jsonify({
            'success': True,
            'assessment': {
                'result': ai_response,
                'skill_area': skill_area,
                'assessment_date': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logging.error(f"Skill assessment error: {e}")
        return jsonify({
            'success': False,
            'error': 'Skill assessment service unavailable'
        }), 500

@skills_bp.route('/api/learning-feedback', methods=['POST'])
def learning_feedback():
    """Provide AI feedback on learning exercises"""
    try:
        data = request.get_json()
        lesson_id = data.get('lesson_id', '')
        user_answer = data.get('answer', '')
        lesson_topic = data.get('topic', '')
        
        if not user_answer:
            return jsonify({
                'success': False,
                'error': 'Answer is required for feedback'
            }), 400
        
        # Create feedback prompt
        prompt = f"""
        Provide constructive feedback on this learning exercise response:
        
        Lesson Topic: {lesson_topic}
        Student Response: {user_answer}
        
        Please provide:
        1. Positive aspects of the response
        2. Areas for improvement
        3. Specific suggestions for enhancement
        4. Additional resources or next steps
        
        Keep feedback encouraging and focused on practical application.
        """
        
        ai_feedback = general_chat_response(prompt, "Learning feedback")
        
        return jsonify({
            'success': True,
            'feedback': ai_feedback,
            'lesson_id': lesson_id
        })
        
    except Exception as e:
        logging.error(f"Learning feedback error: {e}")
        return jsonify({
            'success': False,
            'error': 'Feedback service unavailable'
        }), 500
