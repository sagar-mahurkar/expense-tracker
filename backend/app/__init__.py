from dotenv import load_dotenv

load_dotenv()

from flask import Flask

from app.config.settings import Config
from app.database.initializer import initialize_database
from app.extensions import db
from app.modules.health.route import health_bp

from app.errors.handlers import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    initialize_database()
    db.init_app(app)
    
    register_error_handlers(app)
        
    app.register_blueprint(health_bp)
    
    return app
