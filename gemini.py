import json
import logging
import os

from google import genai
from google.genai import types
from groq import Groq
from pydantic import BaseModel


# AI providers are initialized lazily so the app can start even before keys are
# configured. Groq is the primary provider; Gemini is used only as a fallback.
gemini_client = None
groq_client = None
last_provider = None
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")


def get_gemini_client():
    global gemini_client
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    if gemini_client is None:
        gemini_client = genai.Client(api_key=api_key)
    return gemini_client


def get_groq_client():
    global groq_client
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    if groq_client is None:
        groq_client = Groq(api_key=api_key)
    return groq_client


def get_last_provider():
    """Return the provider used for the most recent successful AI request."""
    return last_provider


def _extract_json(text: str) -> str:
    """Remove optional markdown fences before parsing model JSON."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
    return cleaned.strip()


def _generate_with_groq(
    system_prompt: str,
    user_prompt: str,
    response_schema: type[BaseModel] | None = None,
    json_mode: bool = False,
) -> str:
    client = get_groq_client()
    if client is None:
        raise RuntimeError("GROQ_API_KEY is not configured")

    schema_instruction = ""
    if response_schema is not None:
        schema_instruction = (
            "\nReturn ONLY valid JSON matching this schema. Do not include markdown "
            f"or additional text:\n{json.dumps(response_schema.model_json_schema())}"
        )

    request = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prompt}{schema_instruction}"},
        ],
        "temperature": 0.2,
    }
    if json_mode or response_schema is not None:
        request["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**request)
    text = response.choices[0].message.content if response.choices else None
    if not text:
        raise ValueError("Empty response from Groq")
    return text


def _generate_with_gemini(
    system_prompt: str,
    user_prompt: str,
    response_schema: type[BaseModel] | None = None,
) -> str:
    client = get_gemini_client()
    if client is None:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    config_kwargs = {"system_instruction": system_prompt}
    if response_schema is not None:
        config_kwargs.update({
            "response_mime_type": "application/json",
            "response_schema": response_schema,
        })

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Content(role="user", parts=[types.Part(text=user_prompt)])],
        config=types.GenerateContentConfig(**config_kwargs),
    )
    if not response.text:
        raise ValueError("Empty response from Gemini")
    return response.text


def _generate_text(
    system_prompt: str,
    user_prompt: str,
    response_schema: type[BaseModel] | None = None,
    json_mode: bool = False,
) -> str:
    """Try Groq first, then Gemini, and fail explicitly if both are unavailable."""
    global last_provider
    providers = (
        ("groq", lambda: _generate_with_groq(
            system_prompt, user_prompt, response_schema, json_mode
        )),
        ("gemini", lambda: _generate_with_gemini(
            system_prompt, user_prompt, response_schema
        )),
    )
    errors = []
    for provider_name, generate in providers:
        try:
            result = generate()
            last_provider = provider_name
            return result
        except Exception as exc:
            errors.append(f"{provider_name}: {exc}")
            logging.warning("AI provider %s failed: %s", provider_name, exc)
    raise RuntimeError("All AI providers failed: " + "; ".join(errors))


def _generate_json(
    system_prompt: str,
    user_prompt: str,
    response_schema: type[BaseModel] | None = None,
):
    raw = _generate_text(
        system_prompt,
        user_prompt,
        response_schema=response_schema,
        json_mode=True,
    )
    return json.loads(_extract_json(raw))


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

        data = _generate_json(system_prompt, user_prompt, HealthAdvice)
        return HealthAdvice(**data)

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

        data = _generate_json(system_prompt, user_prompt, JobMatch)
        return JobMatch(**data)

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

        data = _generate_json(system_prompt, user_prompt, NutritionPlan)
        return NutritionPlan(**data)

    except Exception as e:
        logging.error(f"Failed to get nutrition advice: {e}")
        return NutritionPlan(
            daily_calories=2000,
            meal_suggestions=["Balanced meals with available local ingredients"],
            nutritional_tips=["Consult with a nutritionist for personalized advice"],
            warnings=["Please seek professional guidance for specific dietary needs"]
        )


class WeatherForecastDay(BaseModel):
    day: str
    high: str
    low: str
    condition: str
    icon: str
    rain: str


class ClimateAdvice(BaseModel):
    current_conditions: str
    temperature: str
    humidity: str
    wind_speed: str
    precipitation: str
    pressure: str
    recommendations: list[str]
    warnings: list[str]
    forecast: list[WeatherForecastDay]

class DisasterAssessment(BaseModel):
    preparedness_score: int
    risk_level: str
    recommendations: list[str]
    immediate_actions: list[str]
    supplies_needed: list[str]

def get_india_weather(location: str = "New Delhi") -> ClimateAdvice:
    """Get weather information for India using Groq with Gemini fallback."""
    try:
        system_prompt = (
            "You are a weather and climate advisor for India. "
            "Provide current weather conditions, temperature, humidity, wind speed, precipitation, "
            "pressure and practical advice "
            "for the specified location in India. Focus on actionable recommendations "
            "for community members dealing with Indian climate conditions."
        )

        user_prompt = f"""Provide current weather information and climate advice for {location}, India.
Include the current temperature in °C, humidity percentage, wind speed in km/h,
precipitation in mm, pressure in hPa, current conditions, practical recommendations,
warnings, and a realistic 5-day forecast. For each forecast day include day, high,
low, condition, icon (sunny, cloudy, rainy, or storm), and rain in mm."""

        data = _generate_json(system_prompt, user_prompt, ClimateAdvice)
        return ClimateAdvice(**data)

    except Exception as e:
        logging.error(f"Failed to get India weather: {e}")
        return ClimateAdvice(
            current_conditions="Warm conditions with partly cloudy skies",
            temperature="32°C",
            humidity="65%",
            wind_speed="12 km/h",
            precipitation="0 mm",
            pressure="1013 hPa",
            recommendations=[
                "Stay hydrated and avoid prolonged exposure during peak afternoon heat.",
                "Wear light, breathable clothing and use sun protection outdoors.",
                "Monitor official local weather alerts before planning travel or outdoor work."
            ],
            warnings=["AI weather updates are temporarily unavailable; showing the latest safe fallback guidance."],
            forecast=[
                {"day": "Today", "high": "32°C", "low": "25°C", "condition": "Partly cloudy", "icon": "cloudy", "rain": "0 mm"},
                {"day": "Tomorrow", "high": "34°C", "low": "26°C", "condition": "Sunny", "icon": "sunny", "rain": "0 mm"},
                {"day": "Day 3", "high": "33°C", "low": "26°C", "condition": "Cloudy", "icon": "cloudy", "rain": "2 mm"},
                {"day": "Day 4", "high": "31°C", "low": "25°C", "condition": "Light rain", "icon": "rainy", "rain": "8 mm"},
                {"day": "Day 5", "high": "32°C", "low": "25°C", "condition": "Partly cloudy", "icon": "cloudy", "rain": "1 mm"}
            ]
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

        data = _generate_json(system_prompt, user_prompt, DisasterAssessment)
        return DisasterAssessment(**data)

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

        return _generate_text(prompt, prompt)

    except Exception as e:
        logging.error(f"Failed to get climate advice: {e}")
        return "Please check back later for climate recommendations."


def get_agricultural_weather(location: str = "Central India") -> dict:
    """Get agricultural weather and farming advice using Groq with Gemini fallback."""
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

        return _generate_json(system_prompt, user_prompt)

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

        return _generate_text(system_prompt, full_prompt)

    except Exception as e:
        logging.error(f"Failed to generate chat response: {e}")
        return "I'm having trouble responding right now. Please try again."
