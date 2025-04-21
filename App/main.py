import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS

from App.database import init_db
from App.config import load_config, configure_uploads, setup_error_handlers

from App.controllers import (
    setup_jwt,
    add_auth_context
)

# Import all view blueprints
from App.views.index import index_views
from App.views.auth import auth_views
from App.views.recipe import recipe_views
from App.views.category import category_views
from App.views.ingredient import ingredient_views
from App.views.review import review_views

def add_views(app):
    # Register all view blueprints
    app.register_blueprint(index_views)
    app.register_blueprint(auth_views)
    app.register_blueprint(recipe_views)
    app.register_blueprint(category_views)
    app.register_blueprint(ingredient_views)
    app.register_blueprint(review_views)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    
    # Configure JWT
    jwt = setup_jwt(app)
    
    # Add auth context
    add_auth_context(app)
    
    # Configure file uploads
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    configure_uploads(app)
    
    # Register views
    add_views(app)
    
    # Initialize database
    init_db(app)
    
    # Setup error handlers
    setup_error_handlers(app, jwt)

    app.app_context().push()
    return app
    