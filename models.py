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


class CourseListing(db.Model):
    """Curated external learning resources for career development."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240), nullable=False)
    provider = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    difficulty_level = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(80))
    is_free = db.Column(db.Boolean, default=False)
    course_url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def seed_defaults(cls):
        courses = [
            ("Python for Everybody", "Coursera", "Learn Python programming from fundamentals through data structures and practical projects.", "Software Engineering", "Beginner", "8 months", False, "https://www.coursera.org/specializations/python"),
            ("Google IT Automation with Python", "Coursera", "Build automation skills with Python, Git, troubleshooting, and configuration management.", "DevOps & IT", "Intermediate", "6 months", False, "https://www.coursera.org/professional-certificates/google-it-automation"),
            ("Meta Back-End Developer", "Coursera", "Develop server-side applications, APIs, databases, and deployment skills for modern web products.", "Backend Engineering", "Intermediate", "8 months", False, "https://www.coursera.org/professional-certificates/meta-back-end-developer"),
            ("IBM DevOps and Software Engineering", "Coursera", "Practice Agile development, containers, CI/CD, microservices, and cloud-native engineering.", "DevOps & Software Engineering", "Intermediate", "14 months", False, "https://www.coursera.org/professional-certificates/ibm-devops-and-software-engineering"),
            ("Machine Learning Specialization", "Coursera", "Build and apply foundational supervised and unsupervised machine learning models.", "AI & Machine Learning", "Intermediate", "3 months", False, "https://www.coursera.org/specializations/machine-learning-introduction"),
            ("The Complete 2024 Web Development Bootcamp", "Udemy", "A practical full-stack path covering HTML, CSS, JavaScript, React, Node, and databases.", "Full-Stack Engineering", "Beginner", "65 hours", False, "https://www.udemy.com/course/the-complete-web-development-bootcamp/"),
            ("100 Days of Code: The Complete Python Pro Bootcamp", "Udemy", "Learn Python through daily projects including automation, APIs, data science, and web development.", "Python Engineering", "Beginner", "60 hours", False, "https://www.udemy.com/course/100-days-of-code/"),
            ("Docker & Kubernetes: The Practical Guide", "Udemy", "Containerize applications and deploy them with Docker, Kubernetes, and production workflows.", "Cloud & DevOps", "Intermediate", "23 hours", False, "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/"),
            ("JavaScript: The Advanced Concepts", "Udemy", "Deepen JavaScript knowledge with closures, asynchronous programming, performance, and architecture.", "Frontend Engineering", "Advanced", "25 hours", False, "https://www.udemy.com/course/advanced-javascript-concepts/"),
        ]
        db.session.add_all(cls(title=t, provider=p, description=d, category=c,
                               difficulty_level=l, duration=du, is_free=f,
                               course_url=u)
                           for t, p, d, c, l, du, f, u in courses)


class MarketplaceProduct(db.Model):
    """External produce references; checkout is handled by the linked seller."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    product_type = db.Column(db.String(40), nullable=False)  # fruit or vegetable
    description = db.Column(db.Text, nullable=False)
    price_label = db.Column(db.String(100))
    seller = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    product_url = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def seed_defaults(cls):
        products = [
            ("Fresh Bananas", "fruit", "Everyday ripe bananas suitable for breakfast, snacks, and smoothies.", "$4.99 / 3 lb", "Amazon Fresh", "Online", "https://www.amazon.com/s?k=bananas+fresh+produce"),
            ("Alphonso Mangoes", "fruit", "Seasonal mangoes with a rich, sweet flavor.", "$12.99 / pack", "Amazon Fresh", "Online", "https://www.amazon.com/s?k=alphonso+mangoes"),
            ("Fresh Apples", "fruit", "Crisp apples for snacks, lunch boxes, and cooking.", "$6.49 / 3 lb", "Amazon Fresh", "Online", "https://www.amazon.com/s?k=fresh+apples+produce"),
            ("Oranges", "fruit", "Juicy oranges with natural vitamin C.", "$5.99 / 4 lb", "Amazon Fresh", "Online", "https://www.amazon.com/s?k=oranges+fresh+produce"),
            ("Papaya", "fruit", "Fresh papaya for fruit bowls and smoothies.", "$5.49 / each", "Amazon Fresh", "Online", "https://www.amazon.com/s?k=fresh+papaya"),
            ("Tomatoes", "vegetable", "Ripe tomatoes for salads, sauces, and cooking.", "$3.99 / 2 lb", "Amazon Fresh", "Online", "https://www.amazon.com/s?k=fresh+tomatoes+produce"),
            ("Spinach", "vegetable", "Washed leafy greens for nutritious meals.", "$3.49 / bag", "Amazon Fresh", "Online", "https://www.amazon.com/s?k=fresh+spinach"),
            ("Carrots", "vegetable", "Crunchy carrots for snacks, soups, and stews.", "$2.99 / 2 lb", "Amazon Fresh", "Online", "https://www.amazon.com/s?k=fresh+carrots+produce"),
            ("Potatoes", "vegetable", "Versatile potatoes for affordable family meals.", "$5.49 / 5 lb", "Amazon Fresh", "Online", "https://www.amazon.com/s?k=potatoes+fresh+produce"),
            ("Onions", "vegetable", "Kitchen staple for everyday cooking.", "$3.99 / 3 lb", "Amazon Fresh", "Online", "https://www.amazon.com/s?k=onions+fresh+produce"),
            ("Broccoli", "vegetable", "Fresh broccoli florets for steaming and roasting.", "$4.99 / 2 crowns", "Amazon Fresh", "Online", "https://www.amazon.com/s?k=fresh+broccoli"),
            ("Bell Peppers", "vegetable", "Colorful peppers for stir-fries, salads, and curries.", "$5.99 / 3 pack", "Amazon Fresh", "Online", "https://www.amazon.com/s?k=bell+peppers+fresh"),
        ]
        db.session.add_all(cls(name=n, product_type=t, description=d, price_label=pr,
                               seller=s, location=loc, product_url=url)
                           for n, t, d, pr, s, loc, url in products)

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

    @classmethod
    def seed_defaults(cls):
        services = [
            ("AIIMS New Delhi", "hospital", "Ansari Nagar, New Delhi", 28.5672, 77.2100, "011-26588500", "24/7", "Emergency care, outpatient services, diagnostics"),
            ("Safdarjung Hospital", "hospital", "Ansari Nagar West, New Delhi", 28.5677, 77.2066, "011-26730000", "24/7", "Emergency care, surgery, maternity"),
            ("Mohalla Clinic - Dwarka", "clinic", "Sector 12, Dwarka, New Delhi", 28.5921, 77.0460, "Local clinic desk", "8:00 AM - 2:00 PM", "Primary care, basic medicines, referrals"),
            ("Jan Aushadhi Pharmacy", "pharmacy", "Connaught Place, New Delhi", 28.6315, 77.2167, "Local pharmacy desk", "9:00 AM - 9:00 PM", "Affordable generic medicines"),
        ]
        db.session.add_all(cls(name=n, service_type=t, address=a, latitude=lat,
                               longitude=lng, contact_info=phone, hours=hours,
                               services_offered=offered)
                           for n, t, a, lat, lng, phone, hours, offered in services)

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
