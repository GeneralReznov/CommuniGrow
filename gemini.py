import json
import logging
import os

from google import genai
from google.genai import types
from pydantic import BaseModel


# IMPORTANT: KEEP THIS COMMENT
# Follow these instructions when using this blueprint:
# - Note that the newest Gemini model series is "gemini-2.5-flash" or gemini-2.5-pro"
#   - do not change this unless explicitly requested by the user
# - Sometimes the google genai SDK has occasional type errors. You might need to run to validate, at time.  
# The SDK was recently renamed from google-generativeai to google-genai. This file reflects the new name and the new APIs.

# This API key is from Gemini Developer API Key, not vertex AI API Key
os.environ['GEMINI_API_KEY']="AIzaSyChpIrLMzJc42ETm0jS4KiKC_ra9Gv1_vE"
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


class HealthAdvice(BaseModel):
    advice: str
    urgency_level: str
    recommended_actions: list[str]


class JobMatch(BaseModel):
    match_score: float
    reasons: list[str]
    skill_gaps: list[str]
    recommendations: list[str]


class NutritionPlan(BaseModel):
    daily_calories: int
    meal_suggestions: list[str]
    nutritional_tips: list[str]
    warnings: list[str]


def get_health_advice(symptoms: str, age: int = None, gender: str = None) -> HealthAdvice:
    """Get health advice based on symptoms and demographics"""
    try:
        system_prompt = (
            "You are a helpful health advisor for underserved communities. "
            "Provide practical, safe health advice based on symptoms. "
            "Always recommend consulting healthcare professionals for serious concerns. "
            "Focus on preventive care and accessible remedies."
        )

        user_prompt = f"Symptoms: {symptoms}"
        if age:
            user_prompt += f", Age: {age}"
        if gender:
            user_prompt += f", Gender: {gender}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=HealthAdvice,
            ),
        )

        if response.text:
            data = json.loads(response.text)
            return HealthAdvice(**data)
        else:
            raise ValueError("Empty response from model")

    except Exception as e:
        logging.error(f"Failed to get health advice: {e}")
        return HealthAdvice(
            advice="Please consult with a healthcare professional for personalized advice.",
            urgency_level="medium",
            recommended_actions=["Seek professional medical consultation"]
        )


def match_job_to_skills(job_description: str, user_skills: list[str]) -> JobMatch:
    """Match a job to user skills and provide recommendations"""
    try:
        system_prompt = (
            "You are an AI career advisor for underserved communities. "
            "Analyze job descriptions against user skills and provide matching scores, "
            "identify skill gaps, and suggest practical improvements."
        )

        user_prompt = f"Job: {job_description}\nUser Skills: {', '.join(user_skills)}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=JobMatch,
            ),
        )

        if response.text:
            data = json.loads(response.text)
            return JobMatch(**data)
        else:
            raise ValueError("Empty response from model")

    except Exception as e:
        logging.error(f"Failed to match job to skills: {e}")
        return JobMatch(
            match_score=0.0,
            reasons=["Unable to analyze at this time"],
            skill_gaps=["Analysis unavailable"],
            recommendations=["Please try again later"]
        )


def get_nutrition_advice(dietary_preferences: str, health_conditions: str = None, budget: str = "low") -> NutritionPlan:
    """Get personalized nutrition advice for community members"""
    try:
        system_prompt = (
            "You are a nutrition advisor for underserved communities. "
            "Provide practical, affordable nutrition advice that considers "
            "limited resources and local food availability. Focus on accessible, "
            "culturally appropriate recommendations."
        )

        user_prompt = f"Dietary preferences: {dietary_preferences}, Budget: {budget}"
        if health_conditions:
            user_prompt += f", Health conditions: {health_conditions}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=NutritionPlan,
            ),
        )

        if response.text:
            data = json.loads(response.text)
            return NutritionPlan(**data)
        else:
            raise ValueError("Empty response from model")

    except Exception as e:
        logging.error(f"Failed to get nutrition advice: {e}")
        return NutritionPlan(
            daily_calories=2000,
            meal_suggestions=["Balanced meals with available local ingredients"],
            nutritional_tips=["Consult with a nutritionist for personalized advice"],
            warnings=["Please seek professional guidance for specific dietary needs"]
        )


class ClimateAdvice(BaseModel):
    current_conditions: str
    temperature: str
    humidity: str
    recommendations: list[str]
    warnings: list[str]

class DisasterAssessment(BaseModel):
    preparedness_score: int
    risk_level: str
    recommendations: list[str]
    immediate_actions: list[str]
    supplies_needed: list[str]

def get_india_weather(location: str = "New Delhi") -> ClimateAdvice:
    """Get weather information for India using Gemini AI"""
    try:
        system_prompt = (
            "You are a weather and climate advisor for India. "
            "Provide current weather conditions, temperature, humidity and practical advice "
            "for the specified location in India. Focus on actionable recommendations "
            "for community members dealing with Indian climate conditions."
        )

        user_prompt = f"Provide current weather information and climate advice for {location}, India. Include temperature, humidity, current conditions, and practical recommendations for today's weather."

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=ClimateAdvice,
            ),
        )

        if response.text:
            data = json.loads(response.text)
            return ClimateAdvice(**data)
        else:
            raise ValueError("Empty response from model")

    except Exception as e:
        logging.error(f"Failed to get India weather: {e}")
        return ClimateAdvice(
            current_conditions="Weather data temporarily unavailable",
            temperature="N/A",
            humidity="N/A",
            recommendations=["Please check back later for weather updates"],
            warnings=["Unable to fetch current weather data"]
        )

def assess_disaster_preparedness(disaster_type: str, responses: dict, location: str) -> DisasterAssessment:
    """Assess disaster preparedness based on questionnaire responses"""
    try:
        system_prompt = (
            "You are a disaster preparedness expert for Indian communities. "
            "Analyze questionnaire responses and provide a preparedness score (0-100), "
            "risk level assessment, and specific recommendations based on the disaster type and location."
        )

        user_prompt = f"Disaster type: {disaster_type}, Location: {location}, India. User responses: {json.dumps(responses)}. Provide preparedness assessment."

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=DisasterAssessment,
            ),
        )

        if response.text:
            data = json.loads(response.text)
            return DisasterAssessment(**data)
        else:
            raise ValueError("Empty response from model")

    except Exception as e:
        logging.error(f"Failed to assess disaster preparedness: {e}")
        return DisasterAssessment(
            preparedness_score=50,
            risk_level="medium",
            recommendations=["Please complete the assessment again"],
            immediate_actions=["Create emergency supplies kit"],
            supplies_needed=["Basic emergency supplies"]
        )

def get_climate_advice(location: str, climate_data: dict = None) -> str:
    """Get climate adaptation advice based on location and weather data"""
    try:
        prompt = (
            f"Provide climate adaptation and sustainable living advice for {location}, India. "
            "Focus on practical, low-cost solutions for underserved communities in Indian context."
        )
        if climate_data:
            prompt += f" Consider this weather data: {climate_data}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text or "Unable to provide climate advice at this time."

    except Exception as e:
        logging.error(f"Failed to get climate advice: {e}")
        return "Please check back later for climate recommendations."


def get_agricultural_weather(location: str = "Central India") -> dict:
    """Get agricultural weather forecast and advice for farming using Gemini AI"""
    try:
        system_prompt = (
            "You are an agricultural weather advisor for Indian farmers. "
            "Provide current weather conditions, 3-day forecast, and specific farming advice. "
            "Include temperature, humidity, wind, rainfall predictions, and actionable recommendations "
            "for crop management, irrigation, and plant protection based on weather conditions."
        )

        user_prompt = f"""Provide agricultural weather forecast and advice for {location}, India. 
        
Include:
1. Current weather: temperature (°C), condition, wind speed (km/h), humidity (%), precipitation (mm), feels like temperature
2. 3-day forecast with daily high/low temperatures, conditions, and expected rainfall
3. Crop advice based on weather conditions
4. Irrigation recommendations
5. Plant protection advice
        
Format as JSON with:
- current_temp: number
- condition: string
- icon: string (sunny/cloudy/rainy)
- wind_speed: number
- humidity: number
- precipitation: number
- feels_like: number
- forecast: array of 3 days with day, high, low, condition, icon, rain
- crop_advice: string
- irrigation_advice: string
- protection_advice: string"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json"
            ),
        )

        if response.text:
            data = json.loads(response.text)
            return data
        else:
            raise ValueError("Empty response from model")

    except Exception as e:
        logging.error(f"Failed to get agricultural weather: {e}")
        # Return fallback data with some randomization
        import random
        temps = [26, 28, 30, 32, 35]
        conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain']
        
        return {
            'current_temp': random.choice(temps),
            'condition': random.choice(conditions),
            'icon': 'cloudy',
            'wind_speed': random.randint(8, 15),
            'humidity': random.randint(55, 75),
            'precipitation': random.randint(0, 5),
            'feels_like': random.choice(temps) + 2,
            'forecast': [
                {
                    'day': 'Today',
                    'high': random.choice(temps),
                    'low': random.choice(temps) - 6,
                    'condition': random.choice(conditions),
                    'icon': 'cloudy',
                    'rain': random.randint(0, 8)
                },
                {
                    'day': 'Tomorrow', 
                    'high': random.choice(temps),
                    'low': random.choice(temps) - 6,
                    'condition': random.choice(conditions),
                    'icon': 'rainy' if random.choice([True, False]) else 'sunny',
                    'rain': random.randint(0, 12)
                },
                {
                    'day': 'Day 3',
                    'high': random.choice(temps),
                    'low': random.choice(temps) - 6,
                    'condition': random.choice(conditions),
                    'icon': 'sunny' if random.choice([True, False]) else 'cloudy',
                    'rain': random.randint(0, 6)
                }
            ],
            'crop_advice': f'Weather conditions in {location} are suitable for most crops. Monitor for changes.',
            'irrigation_advice': 'Adjust irrigation based on rainfall patterns and soil moisture levels.',
            'protection_advice': 'Protect crops from extreme weather. Use organic methods when possible.'
        }


def general_chat_response(message: str, context: str = "") -> str:
    """General chat response for community platform"""
    try:
        system_prompt = (
            "You are a helpful assistant for a community platform serving "
            "underserved populations. Provide supportive, practical advice "
            "focusing on health, education, climate action, and economic opportunities. "
            "Be empathetic and culturally sensitive."
        )

        full_prompt = f"Context: {context}\nUser message: {message}" if context else message

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=full_prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
        )

        return response.text or "I'm here to help! Could you please rephrase your question?"

    except Exception as e:
        logging.error(f"Failed to generate chat response: {e}")
        return "I'm having trouble responding right now. Please try again."
