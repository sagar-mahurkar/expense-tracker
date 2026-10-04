from flask import Flask

from app.config.settings import Config
from app.modules.health.route import health_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(health_bp)
    
    return app