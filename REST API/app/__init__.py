# app/__init__.py
from flask import Flask, render_template
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register routes
    from app.routes import register_routes
    register_routes(app)
    return app
