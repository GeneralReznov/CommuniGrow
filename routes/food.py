from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import logging
import uuid
from datetime import datetime
from models import FoodListing
from app import db
from gemini import get_nutrition_advice, general_chat_response

food_bp = Blueprint('food', __name__)

@food_bp.route('/')
def index():
    """Food and nutrition module main page"""
    recent_listings = FoodListing.query.filter_by(is_available=True).order_by(FoodListing.created_at.desc()).limit(6).all()
    return render_template('food/index.html', recent_listings=recent_listings)

@food_bp.route('/marketplace')
def marketplace():
    """Farmer-to-consumer marketplace"""
    marketplace_items = FoodListing.query.filter_by(category='marketplace', is_available=True).all()
    sharing_items = FoodListing.query.filter_by(category='sharing', is_available=True).all()
    surplus_items = FoodListing.query.filter_by(category='surplus', is_available=True).all()
    
    return render_template('food/marketplace.html', 
                         marketplace_items=marketplace_items,
                         sharing_items=sharing_items,
                         surplus_items=surplus_items)

@food_bp.route('/nutrition')
def nutrition():
    """Nutrition guidance and meal planning"""
    return render_template('food/nutrition.html')

@food_bp.route('/api/nutrition-advice', methods=['POST'])
def nutrition_advice():
    """Get AI-powered nutrition advice"""
    try:
        data = request.get_json()
        dietary_preferences = data.get('dietary_preferences', '')
        health_conditions = data.get('health_conditions', '')
        budget = data.get('budget', 'low')
        
        if not dietary_preferences:
            return jsonify({
                'success': False,
                'error': 'Dietary preferences are required'
            }), 400
        
        # Get AI nutrition advice
        nutrition_plan = get_nutrition_advice(dietary_preferences, health_conditions, budget)
        
        return jsonify({
            'success': True,
            'daily_calories': nutrition_plan.daily_calories,
            'meal_suggestions': nutrition_plan.meal_suggestions,
            'nutritional_tips': nutrition_plan.nutritional_tips,
            'warnings': nutrition_plan.warnings
        })
    except Exception as e:
        logging.error(f"Nutrition advice error: {e}")
        return jsonify({
            'success': False,
            'error': 'Nutrition service unavailable'
        }), 500

@food_bp.route('/post-listing', methods=['GET', 'POST'])
def post_listing():
    """Post a new food listing"""
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            
            listing = FoodListing(
                title=data.get('title'),
                description=data.get('description'),
                category=data.get('category'),
                price=float(data.get('price', 0)) if data.get('price') else None,
                quantity=data.get('quantity'),
                location=data.get('location'),
                contact_info=data.get('contact_info')
            )
            
            db.session.add(listing)
            db.session.commit()
            
            if request.is_json:
                return jsonify({
                    'success': True,
                    'message': 'Listing posted successfully'
                })
            else:
                return redirect(url_for('food.marketplace'))
        except Exception as e:
            logging.error(f"Food listing error: {e}")
            if request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Failed to post listing'
                }), 500
            else:
                return render_template('food/marketplace.html', error='Failed to post listing')
    
    return render_template('food/marketplace.html', show_form=True)

@food_bp.route('/recipes')
def recipes():
    """Community recipes and cooking tips"""
    recipes = {
        'budget_friendly': [
            {
                'name': 'Lentil and Vegetable Stew',
                'ingredients': ['1 cup lentils', '2 cups mixed vegetables', 'Spices', 'Water'],
                'instructions': 'Boil lentils, add vegetables and spices, simmer for 20 minutes',
                'nutrition': 'High protein, fiber, vitamins'
            },
            {
                'name': 'Rice and Bean Bowl',
                'ingredients': ['1 cup rice', '1 cup beans', 'Onions', 'Garlic', 'Oil'],
                'instructions': 'Cook rice and beans separately, sauté onions and garlic, combine',
                'nutrition': 'Complete protein, carbohydrates, minerals'
            }
        ],
        'preservation': [
            {
                'method': 'Solar Drying',
                'description': 'Use sun energy to dry fruits and vegetables for long-term storage',
                'equipment': 'Drying racks, clean cloth, sunny location'
            },
            {
                'method': 'Fermentation',
                'description': 'Natural preservation method that adds beneficial bacteria',
                'equipment': 'Clean jars, salt, vegetables'
            }
        ],
        'nutrition_tips': [
            'Include a variety of colorful vegetables in meals',
            'Combine legumes with grains for complete protein',
            'Drink plenty of clean water throughout the day',
            'Use local, seasonal produce when possible',
            'Practice food safety and proper storage'
        ]
    }
    
    return render_template('food/nutrition.html', recipes=recipes)

@food_bp.route('/food-safety')
def food_safety():
    """Food safety and storage guidelines"""
    safety_guidelines = {
        'storage': [
            'Keep raw and cooked foods separate',
            'Store food at proper temperatures',
            'Use airtight containers for dry goods',
            'Check expiration dates regularly',
            'Keep storage areas clean and dry'
        ],
        'preparation': [
            'Wash hands before handling food',
            'Clean all surfaces and utensils',
            'Cook food to safe temperatures',
            'Avoid cross-contamination',
            'Use clean water for cooking and washing'
        ],
        'emergency': [
            'Know signs of food spoilage',
            'Have emergency food supplies',
            'Understand water purification methods',
            'Keep first aid supplies accessible',
            'Know local emergency contacts'
        ]
    }
    
    return render_template('food/nutrition.html', safety_guidelines=safety_guidelines)

@food_bp.route('/chat')
def agricultural_chat():
    """Agricultural AI chat assistant"""
    return render_template('food/chat.html')

@food_bp.route('/weather')
def weather_forecast():
    """Agricultural weather forecast"""
    return render_template('food/weather.html')

@food_bp.route('/water')
def water_management():
    """Water management system"""
    return render_template('food/water.html')

@food_bp.route('/prices')
def crop_prices():
    """Crop market prices"""
    return render_template('food/prices.html')

@food_bp.route('/schemes')
def government_schemes():
    """Government agricultural schemes"""
    return render_template('food/schemes.html')

@food_bp.route('/api/agricultural-chat', methods=['POST'])
def agricultural_chat_api():
    """AI-powered agricultural chat assistant"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        # Create agricultural context prompt
        prompt = f"""
        You are an expert agricultural advisor helping farmers and food producers. 
        Provide practical, actionable advice for:
        
        User Question: {message}
        
        Focus on:
        - Sustainable farming practices
        - Crop management and cultivation
        - Soil health and fertilization
        - Pest and disease management
        - Water management and irrigation
        - Market insights and timing
        - Government schemes and support
        
        Keep responses practical and suitable for small to medium scale farmers.
        """
        
        # Get AI response
        ai_response = general_chat_response(prompt, "Agricultural advisory")
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'session_id': str(uuid.uuid4())
        })
        
    except Exception as e:
        logging.error(f"Agricultural chat error: {e}")
        return jsonify({
            'success': False,
            'error': 'Agricultural chat service unavailable'
        }), 500

@food_bp.route('/api/agricultural-weather', methods=['POST'])
def agricultural_weather_api():
    """Agricultural weather forecast API using Gemini AI"""
    try:
        data = request.get_json()
        region = data.get('region', 'Central India')
        days = data.get('days', 3)
        
        if not region:
            return jsonify({
                'success': False,
                'error': 'Region is required'
            }), 400
        
        # Get dynamic weather data using Gemini AI
        from gemini import get_agricultural_weather
        weather_response = get_agricultural_weather(region)
        
        # Extract weather data and agricultural advice from AI response
        weather_data = {
            'current_temp': weather_response.get('current_temp', 28),
            'condition': weather_response.get('condition', 'Partly Cloudy'),
            'icon': weather_response.get('icon', 'cloudy'),
            'wind_speed': weather_response.get('wind_speed', 12),
            'humidity': weather_response.get('humidity', 65),
            'precipitation': weather_response.get('precipitation', 2),
            'feels_like': weather_response.get('feels_like', 31),
            'forecast': weather_response.get('forecast', [])
        }
        
        agricultural_advice = {
            'crop_advice': weather_response.get('crop_advice', 'Weather conditions are suitable for farming activities.'),
            'irrigation_advice': weather_response.get('irrigation_advice', 'Monitor soil moisture and adjust irrigation as needed.'),
            'protection_advice': weather_response.get('protection_advice', 'Protect crops from extreme weather conditions.')
        }
        
        return jsonify({
            'success': True,
            'weather': weather_data,
            'agricultural_advice': agricultural_advice
        })
        
    except Exception as e:
        logging.error(f"Weather forecast error: {e}")
        return jsonify({
            'success': False,
            'error': 'Weather service unavailable'
        }), 500

@food_bp.route('/api/water-management', methods=['POST'])
def water_management_api():
    """Water management planning API"""
    try:
        data = request.get_json()
        crop = data.get('crop', '')
        soil_type = data.get('soil_type', '')
        field_size = data.get('field_size', '')
        season = data.get('season', '')
        location = data.get('location', '')
        
        if not all([crop, soil_type, field_size]):
            return jsonify({
                'success': False,
                'error': 'Crop, soil type, and field size are required'
            }), 400
        
        # Create water management prompt
        prompt = f"""
        Create a comprehensive water management plan for:
        
        Crop: {crop}
        Soil Type: {soil_type}
        Field Size: {field_size} acres
        Season: {season}
        Location: {location}
        
        Provide:
        1. Water requirements and irrigation schedule
        2. Efficient irrigation methods
        3. Water conservation strategies
        4. Seasonal adjustments
        5. Soil-specific recommendations
        
        Focus on practical, cost-effective solutions.
        """
        
        # Get AI response
        plan = general_chat_response(prompt, "Water management planning")
        
        return jsonify({
            'success': True,
            'plan': {
                'recommendations': plan
            }
        })
        
    except Exception as e:
        logging.error(f"Water management error: {e}")
        return jsonify({
            'success': False,
            'error': 'Water management service unavailable'
        }), 500

@food_bp.route('/api/crop-prices', methods=['POST'])
def crop_prices_api():
    """Crop prices API"""
    try:
        data = request.get_json()
        crop = data.get('crop', '')
        region = data.get('region', 'all')
        
        if not crop:
            return jsonify({
                'success': False,
                'error': 'Crop type is required'
            }), 400
        
        # Simulate market prices (in production, integrate with market APIs)
        import random
        
        base_price = {
            'rice': 2500,
            'wheat': 2200,
            'maize': 1800,
            'potato': 1200,
            'onion': 1500,
            'tomato': 2000
        }.get(crop, 2000)
        
        current_price = base_price + random.randint(-200, 300)
        
        price_data = {
            'current': current_price,
            'high': current_price + 150,
            'low': current_price - 100,
            'average': current_price + 25,
            'trend': {
                'direction': random.choice(['up', 'down', 'neutral']),
                'description': random.choice(['Rising', 'Falling', 'Stable']) + ' trend'
            }
        }
        
        regional_prices = [
            {'name': 'North India', 'price': current_price + 50, 'trend': 'up', 'trend_text': '+2.5%', 'status': 'active', 'status_text': 'Active'},
            {'name': 'South India', 'price': current_price - 30, 'trend': 'down', 'trend_text': '-1.2%', 'status': 'active', 'status_text': 'Active'},
            {'name': 'West India', 'price': current_price + 20, 'trend': 'neutral', 'trend_text': '0.5%', 'status': 'active', 'status_text': 'Active'}
        ]
        
        analysis = {
            'market_analysis': f'Current {crop} prices are showing moderate fluctuation with seasonal demand patterns affecting regional markets.',
            'recommendations': 'Consider holding stock for 2-3 weeks if prices are trending upward. Monitor weather forecasts for supply impact.',
            'seasonal_outlook': 'Harvest season typically sees price drops, while demand increases during festivals and processing seasons.'
        }
        
        return jsonify({
            'success': True,
            'prices': price_data,
            'regional_prices': regional_prices,
            'analysis': analysis
        })
        
    except Exception as e:
        logging.error(f"Crop prices error: {e}")
        return jsonify({
            'success': False,
            'error': 'Price service unavailable'
        }), 500

@food_bp.route('/api/government-schemes', methods=['POST'])
def government_schemes_api():
    """Government schemes finder API"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        farming_type = data.get('farming_type', '')
        location = data.get('location', '')
        language = data.get('language', 'English')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
        
        # Create schemes search prompt
        prompt = f"""
        Find relevant Indian government agricultural schemes based on:
        
        Query: {query}
        Farming Type: {farming_type}
        Location: {location}
        Language: {language}
        
        Provide information about:
        1. Scheme names and descriptions
        2. Eligibility criteria
        3. Benefits and support provided
        4. Application process
        5. Contact information
        
        Focus on currently active schemes and provide practical guidance.
        Respond in {language} language.
        """
        
        # Get AI response
        schemes_info = general_chat_response(prompt, "Government schemes search")
        
        return jsonify({
            'success': True,
            'schemes': {
                'recommendations': schemes_info
            }
        })
        
    except Exception as e:
        logging.error(f"Government schemes error: {e}")
        return jsonify({
            'success': False,
            'error': 'Schemes service unavailable'
        }), 500
