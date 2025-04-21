from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request, set_access_cookies, unset_jwt_cookies
from flask import redirect, url_for, flash

from App.models import User

def login(username, password):
    try:
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Ensure identity is a string
            return create_access_token(identity=str(user.id))
        return None
    except Exception as e:
        print(f"Login error: {str(e)}")
        return None


def setup_jwt(app):
    jwt = JWTManager(app)

    # configure's flask jwt to resolve get_current_identity() to the corresponding user's ID
    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        # Ensure identity is a string
        return str(identity)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        # Convert string identity back to integer for database lookup
        return User.query.get(int(identity))

    return jwt


# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
    @app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                current_user = User.query.get(int(user_id))
                is_authenticated = True
            else:
                is_authenticated = False
                current_user = None
        except Exception as e:
            print(e)
            is_authenticated = False
            current_user = None
        return dict(is_authenticated=is_authenticated, current_user=current_user)

def logout():
    """Logout the current user by clearing JWT cookies"""
    response = redirect('/')
    unset_jwt_cookies(response)
    flash('Logged out successfully', 'success')
    return response