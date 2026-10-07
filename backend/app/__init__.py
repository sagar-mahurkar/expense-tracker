from dotenv import load_dotenv

load_dotenv()

from flask import Flask

from app.config.settings import Config
from app.database.initializer import initialize_database
from app.extensions import db, jwt
from app.modules.health.route import health_bp

from app.errors.handlers import register_error_handlers
from app.modules.auth.route import auth_bp
from app.modules.categories.route import categories_bp
from app.modules.transactions.route import transactions_bp
from app.modules.summary.route import summary_bp
from app.config.jwt import configure_jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    initialize_database()
    db.init_app(app)
    jwt.init_app(app)
    configure_jwt(jwt)
    
    register_error_handlers(app)
        
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(summary_bp)
    
    return app
