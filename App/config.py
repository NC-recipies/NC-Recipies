import os
from flask import render_template

def load_config(app, overrides):
    if os.path.exists(os.path.join('./App', 'custom_config.py')):
        app.config.from_object('App.custom_config')
    else:
        app.config.from_object('App.default_config')
    app.config.from_prefixed_env()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    
    # File Upload Configuration
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 604800  # 1 week
    app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']
    app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_COOKIE_SAMESITE'] = 'Lax'
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
    
    # Apply any overrides
    for key in overrides:
        app.config[key] = overrides[key]

def configure_uploads(app):
    """Configure file upload settings"""
    from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    return photos

def setup_error_handlers(app, jwt):
    """Configure error handlers"""
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return render_template('401.html', error="Your session has expired. Please log in again."), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return render_template('401.html', error="Invalid token. Please log in again."), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return render_template('401.html', error="Please log in to access this page."), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return render_template('401.html', error="Your session has expired. Please log in again."), 401