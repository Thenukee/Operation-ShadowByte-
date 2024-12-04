from flask import Flask, send_from_directory
from .routes import api
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__, static_folder='static')

    # Enable CORS for API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register Blueprint
    app.register_blueprint(api, url_prefix='/api')

    # Serve index.html at '/'
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    # Serve static files (CSS, JS, images)
    @app.route('/static/<path:path>')
    def send_static_files(path):
        return send_from_directory(app.static_folder, path)

    return app
