from flask import Flask
from flask_cors import CORS
from config import config


def create_app(config_name='development'):
    """Application factory pattern"""

    app = Flask(__name__,
                static_folder='static',
                static_url_path='/static')

    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Enable CORS - allow all origins for development
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Content-Length"]
        }
    })

    # Register blueprints
    from app.controllers import garment_bp, outfit_bp, chat_bp, tryon_bp

    app.register_blueprint(garment_bp)
    app.register_blueprint(outfit_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(tryon_bp)

    # Health check endpoint
    @app.route('/')
    def index():
        return {
            'message': 'Wardrobe AI Backend API',
            'version': '1.0.0',
            'endpoints': {
                'garments': '/api/garments',
                'outfits': '/api/outfits',
                'chat': '/api/chat',
                'tryon': '/api/tryon'
            }
        }

    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200

    # Additional static file serving route for images
    from flask import send_from_directory
    import os

    @app.route('/static/uploads/<path:filename>')
    def serve_upload(filename):
        """Serve uploaded files directly"""
        upload_folder = app.config.get('UPLOAD_FOLDER') or config[config_name].UPLOAD_FOLDER
        return send_from_directory(upload_folder, filename)

    return app
