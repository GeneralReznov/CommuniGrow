import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
os.environ['DATABASE_URL']="postgresql://neondb_owner:npg_yBCOGRprn97M@ep-long-breeze-a6yx82vz.us-west-2.aws.neon.tech/neondb?sslmode=require"
database_url = os.environ["DATABASE_URL"]
if database_url and database_url.startswith("postgres://"):
    # Fix Heroku postgres URL to be compatible with SQLAlchemy
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///community_platform.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Import models here before creating tables
import models  # noqa: F401

with app.app_context():
    # Create all tables
    db.create_all()

# Register blueprints
from routes.main import main_bp
from routes.climate import climate_bp
from routes.skills import skills_bp
from routes.food import food_bp
from routes.health import health_bp
from routes.payments import payments_bp

app.register_blueprint(main_bp)
app.register_blueprint(climate_bp, url_prefix='/climate')
app.register_blueprint(skills_bp, url_prefix='/skills')
app.register_blueprint(food_bp, url_prefix='/food')
app.register_blueprint(health_bp, url_prefix='/health')
app.register_blueprint(payments_bp, url_prefix='/payments')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
