# CommuniGrow Documentation

## Overview

The CommuniGrow is a comprehensive web application designed to empower underserved communities through technology. Built with Flask and powered by AI (Google Gemini), it provides accessible solutions across four core areas: Climate Action, Skills Development, Food Security, and Healthcare Access.

## Mission Statement

Our platform addresses critical Sustainable Development Goals by providing voice-enabled, AI-powered solutions that are accessible to users with varying technical backgrounds. We focus on practical, community-centered approaches to sustainable development.

## System Architecture

### Backend Technology Stack

- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite (development) / PostgreSQL (production)
- **AI Integration**: Google Gemini API for natural language processing and intelligent responses
- **Authentication**: Flask sessions with configurable security
- **Architecture Pattern**: Blueprint-based modular routing for scalability

### Frontend Technology Stack

- **Template Engine**: Jinja2 for server-side rendering
- **CSS Framework**: Bootstrap 5 for responsive design
- **JavaScript**: Vanilla JavaScript with modular architecture
- **Accessibility**: Web Speech API for voice navigation and text-to-speech
- **Icons**: Font Awesome for consistent iconography
- **Maps**: Leaflet.js for interactive mapping features

### File Structure

```
├── app.py                  # Main Flask application setup
├── main.py                 # Application entry point
├── models.py               # Database models and schemas
├── gemini.py               # AI integration with Google Gemini
├── routes/                 # Modular route blueprints
│   ├── main.py            # Landing page and core routes
│   ├── climate.py         # Climate action module
│   ├── skills.py          # Skills and employment module
│   ├── food.py            # Food and nutrition module
│   ├── health.py          # Health and wellbeing module
│   └── payments.py        # Payment processing (Stripe)
├── templates/             # HTML templates organized by module
├── static/               # CSS, JavaScript, and assets
└── instance/             # Database and configuration files
```

## App Link:https://communigrow.onrender.com/

## Core Modules

### 1. Climate Action & Sustainability Module (`/climate`)

**Purpose**: Empowers communities with climate resilience and environmental sustainability tools.

**Key Features**:

- **Real-time Weather Monitoring**: AI-powered weather data for India with location-specific forecasts
- **Disaster Preparedness Assessment**: Interactive questionnaires that provide personalized preparedness scores and recommendations
- **Climate Alerts System**: Community-wide alerts for weather emergencies and climate events
- **Sustainable Practices Guide**: Practical advice for farming, energy efficiency, and water conservation
- **Environmental Sensor Integration**: Support for IoT sensors (air quality, water quality, solar energy)

**API Endpoints**:
- `GET /climate/api/weather/<location>` - Weather data for Indian locations
- `POST /climate/api/disaster-assessment` - Submit disaster preparedness assessment
- `POST /climate/api/alerts` - Create weather alerts
- `GET /climate/api/iot-sensors` - IoT sensor data

**Database Models**:
- `WeatherAlert`: Store and manage climate alerts
- `DisasterPreparednessAssessment`: Track community preparedness levels

### 2. Skills & Employment Development Module (`/skills`)

**Purpose**: Bridges the employment gap through AI-powered job matching and skill development.

**Key Features**:

- **AI Job Matching**: Intelligent matching between job descriptions and user skills with gap analysis
- **Microlearning Platform**: Bite-sized learning modules for digital literacy, entrepreneurship, and technical skills
- **Interactive Skills Assessment**: AI-powered evaluation with personalized recommendations
- **Career Development Planning**: Comprehensive career roadmaps with milestone tracking
- **Community Job Board**: Local job listings and skill-sharing opportunities
- **Volunteer Opportunities**: Community engagement and skill-building through service

**API Endpoints**:
- `POST /skills/api/job-match` - AI-powered job matching
- `POST /skills/api/career-plan` - Generate career development plans
- `POST /skills/api/skill-assessment` - Skill level assessment
- `POST /skills/api/learning-feedback` - AI feedback on learning exercises

**Database Models**:
- `JobListing`: Job opportunities and requirements
- `SkillListing`: Community skill sharing offerings

### 3. Food & Nutrition Security Module (`/food`)

**Purpose**: Addresses food insecurity through smart marketplace, nutrition guidance, and agricultural support.

**Key Features**:

- **Community Marketplace**: Farmer-to-consumer direct sales platform
- **Food Sharing Network**: Surplus food redistribution system
- **AI Nutrition Advisor**: Personalized meal planning based on dietary needs and budget constraints
- **Agricultural Weather Service**: Crop-specific weather forecasts and farming advice
- **Water Management Planning**: Irrigation optimization and water conservation strategies
- **Crop Price Monitoring**: Real-time market prices and trend analysis
- **Government Schemes Finder**: Agricultural subsidy and support program discovery

**API Endpoints**:
- `POST /food/api/nutrition-advice` - AI nutrition recommendations
- `POST /food/api/agricultural-chat` - Agricultural advisory chatbot
- `POST /food/api/agricultural-weather` - Farming weather forecasts
- `POST /food/api/water-management` - Water management planning
- `POST /food/api/crop-prices` - Market price information
- `POST /food/api/government-schemes` - Government program search

**Database Models**:
- `FoodListing`: Marketplace items and food sharing posts

### 4. Health & Well-being Module (`/health`)

**Purpose**: Provides accessible healthcare through AI-powered guidance and telemedicine support.

**Key Features**:

- **AI Health Chatbot**: Symptom analysis and health advice with urgency level assessment
- **Mental Health Screening**: Evidence-based assessments (PHQ-9, GAD-7, PSS-10) with AI-powered recommendations
- **Sleep Wellness Tracking**: Comprehensive sleep quality analysis with improvement suggestions
- **Telemedicine Platform**: Remote consultation scheduling and support
- **Medical Facility Finder**: Interactive map of local healthcare providers
- **Emergency Information Hub**: Critical health information and emergency contacts
- **Maternal Health Resources**: Pregnancy, childbirth, and child development support

**API Endpoints**:
- `POST /health/api/health-chat` - AI health consultation
- `GET /health/api/health-services` - Healthcare provider listings
- `GET /health/api/nearby-facilities` - Location-based medical facility search

**Database Models**:
- `HealthService`: Healthcare provider information
- `ChatSession`: Health consultation history
- `MentalHealthScreening`: Mental health assessment results
- `SleepWellnessData`: Sleep tracking and analysis
- `TelemedicineSession`: Remote consultation management

## AI Integration Features

### Google Gemini API Integration

The platform leverages Google's Gemini 2.5 Pro and Flash models for various AI-powered features:

**Structured AI Responses**:
- Health advice with urgency levels and action items
- Job matching with compatibility scores and skill gap analysis
- Nutrition planning with meal suggestions and warnings
- Climate advice with location-specific recommendations
- Disaster preparedness assessment with risk levels

**AI-Powered Chat Systems**:
- Health symptom analysis and medical guidance
- Agricultural advisory for farming and crop management
- General community support and information

**Smart Data Processing**:
- Natural language processing for user queries
- Intelligent content generation for community needs
- Personalized recommendations based on user context

## Accessibility Features

### Voice Navigation System

- **Text-to-Speech**: All content can be read aloud using Web Speech API
- **Speech-to-Text**: Voice input for forms and navigation
- **Voice Tour**: Guided audio tour of platform features
- **Keyboard Navigation**: Full keyboard accessibility support
- **High Contrast Mode**: Enhanced visibility for visually impaired users

### Multi-language Support

- Interface designed for easy localization
- AI responses can be provided in local languages
- Cultural sensitivity in content and recommendations

## Database Schema

### Core Tables

1. **WeatherAlert**: Climate emergency notifications
2. **SkillListing**: Community skill sharing
3. **JobListing**: Employment opportunities
4. **FoodListing**: Marketplace and food sharing
5. **HealthService**: Healthcare provider directory
6. **ChatSession**: AI conversation history
7. **MentalHealthScreening**: Mental health assessment data
8. **SleepWellnessData**: Sleep quality tracking
9. **TelemedicineSession**: Remote healthcare sessions
10. **DisasterPreparednessAssessment**: Community preparedness tracking

## Payment Integration

### Stripe Payment Processing

- Secure marketplace transactions
- Support for local and international payments
- Webhook handling for payment verification
- Success/failure handling with appropriate redirects

## Security Features

- **Environment Variables**: Secure API key management
- **Session Management**: Secure user sessions
- **Input Validation**: Protection against malicious input
- **HTTPS Support**: Secure data transmission
- **Database Security**: SQL injection prevention through ORM

## Development Workflow

### Local Development

1. **Application Entry**: `main.py` imports Flask app from `app.py`
2. **Database Initialization**: Automatic table creation on startup
3. **Blueprint Registration**: Modular route organization
4. **AI Service Integration**: Gemini API configuration and error handling

### Production Deployment

- **Gunicorn WSGI Server**: Production-ready application serving
- **Database Migration**: PostgreSQL support for production
- **Environment Configuration**: Secure credential management
- **Reverse Proxy Support**: ProxyFix middleware for deployment

## API Documentation

### Authentication

Currently uses session-based authentication. API endpoints are accessible without authentication for community access, with plans for optional user accounts.

### Rate Limiting

AI API calls are managed to prevent abuse while ensuring availability for community members.

### Error Handling

Comprehensive error handling with graceful degradation:
- AI service failures provide fallback responses
- Database errors return user-friendly messages
- Network issues handled with retry mechanisms

## Community Impact Features

### Sustainable Development Goals Alignment

- **SDG 1**: Poverty reduction through economic opportunities
- **SDG 2**: Food security through marketplace and nutrition guidance
- **SDG 3**: Health and well-being through accessible healthcare
- **SDG 4**: Education through skills development platform
- **SDG 13**: Climate action through environmental monitoring and guidance

### Offline Capabilities

- Critical information cached for offline access
- Progressive Web App features for mobile users
- Essential health and emergency information always available

## Future Enhancements

### Planned Features

1. **Mobile Application**: Native iOS and Android apps
2. **Advanced IoT Integration**: Environmental sensor networks
3. **Blockchain Integration**: Transparent supply chain tracking
4. **Machine Learning**: Predictive analytics for community needs
5. **Multi-tenant Architecture**: Support for multiple communities
6. **Enhanced Collaboration**: Community forums and group features

### Scalability Considerations

- **Microservices Architecture**: Planned transition for larger scale
- **Caching Layer**: Redis integration for performance
- **Content Delivery Network**: Static asset optimization
- **Load Balancing**: Multi-instance deployment support

## Installation and Setup

### Requirements

- Python 3.11+
- Flask and associated packages (see `requirements.txt`)
- Google Gemini API key
- Stripe account (for payments)
- PostgreSQL (production) or SQLite (development)

### Environment Variables

```bash
GEMINI_API_KEY=your_gemini_api_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret
DATABASE_URL=your_database_url
SESSION_SECRET=your_session_secret
```

### Running the Application

```bash
# Development
python main.py

# Production
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## Contributing Guidelines

### Code Organization

- Follow Flask blueprint patterns for new features
- Maintain separation between AI logic and web routes
- Use SQLAlchemy models for all database interactions
- Implement proper error handling and logging

### Testing

- Test AI integrations with fallback scenarios
- Validate accessibility features across browsers
- Test voice navigation on various devices
- Ensure mobile responsiveness

### Documentation

- Update this documentation for new features
- Comment complex AI integration code
- Maintain API endpoint documentation
- Document database schema changes

## Support and Community

### User Support

- In-app help system with voice guidance
- Community forums for peer support
- Documentation and tutorials
- Emergency contact information

### Technical Support

- Error logging and monitoring
- Performance tracking
- User feedback collection
- Continuous improvement based on community needs

## Conclusion

Build during HackOdisha 5.0 so special thanks to them for letting me work on this beautiful project.

The CommuniGrow represents a comprehensive approach to community development through technology. By combining AI-powered insights with accessible design and practical features, it addresses real-world challenges faced by underserved communities while promoting sustainable development and self-empowerment.

The platform's modular architecture allows for continuous expansion and adaptation to specific community needs, while maintaining a focus on accessibility, sustainability, and meaningful impact.
