#!/usr/bin/env python3
"""
Wardrobe AI Backend Server
Main entry point for running the Flask application
"""

import os
from app import create_app

# Get environment from environment variable
env = os.getenv('FLASK_ENV', 'development')

# Create Flask app
app = create_app(env)

if __name__ == '__main__':
    # Get host and port from environment or use defaults
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'

    print(f"""
    ╔══════════════════════════════════════════╗
    ║     Wardrobe AI Backend Server          ║
    ║                                          ║
    ║  Environment: {env:<26} ║
    ║  Host: {host:<33} ║
    ║  Port: {port:<33} ║
    ║  Debug: {str(debug):<32} ║
    ╚══════════════════════════════════════════╝

    API Endpoints:
    - Garments: http://{host}:{port}/api/garments
    - Outfits:  http://{host}:{port}/api/outfits
    - Chat:     http://{host}:{port}/api/chat
    - Try-On:   http://{host}:{port}/api/tryon

    Starting server...
    """)

    app.run(host=host, port=port, debug=debug)
