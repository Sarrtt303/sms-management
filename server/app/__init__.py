from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from config import Config
import logging

# Initialize PyMongo
mongo = PyMongo()

# Initialize JWT
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)

    # Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)

    # Check MongoDB connection
    try:
        # Test the MongoDB connection by executing a command
        mongo.cx.server_info()  # This checks if the MongoDB server is accessible
        logging.info("Successfully connected to MongoDB")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        raise e  # Raise the error so the app doesn't proceed without a DB connection

    # Register blueprints
    from app.api.routes import api_bp
    from app.api.auth import auth_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
