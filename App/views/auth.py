from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies


from.index import index_views

from App.controllers import (
    login,
    create_user,
    get_user_by_username,
    logout
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    

@auth_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@auth_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form
    
    # Validate password match
    if data['password'] != data['confirm_password']:
        flash('Passwords do not match')
        return redirect(url_for('auth_views.signup_page'))
    
    # Check if username exists
    if get_user_by_username(data['username']):
        flash('Username already exists')
        return redirect(url_for('auth_views.signup_page'))
    
    # Create user
    user = create_user(data['username'], data['password'])
    if user:
        # Log the user in immediately after signup
        token = login(data['username'], data['password'])
        response = redirect('/')
        if token:
            set_access_cookies(response, token)
            flash('Account created and logged in successfully!')
            return response
    
    flash('Error creating account')
    return redirect(url_for('auth_views.signup_page'))

@auth_views.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        token = login(username, password)
        if token:
            response = redirect('/')
            set_access_cookies(response, token)
            flash('Login successful!')
            return response
        flash('Invalid username or password')
        return redirect('/login')
    return render_template('login.html', form_action=url_for('auth_views.login_page'))

@auth_views.route('/logout')
@jwt_required()
def logout_page():
    return logout()

'''
API Routes
'''

@auth_views.route('/api/signup', methods=['POST'])
def signup_api():
    data = request.json
    
    # Validate password match
    if data['password'] != data['confirm_password']:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    # Check if username exists
    if get_user_by_username(data['username']):
        return jsonify({'error': 'Username already exists'}), 400
    
    # Create user
    user = create_user(data['username'], data['password'])
    if user:
        return jsonify(user.get_json()), 201
    
    return jsonify({'error': 'Error creating account'}), 400

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
    data = request.json
    token = login(data['username'], data['password'])
    if not token:
        return jsonify(message='bad username or password given'), 401
    response = jsonify(access_token=token) 
    set_access_cookies(response, token)
    return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
@jwt_required()
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response