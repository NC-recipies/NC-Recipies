from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import (
    create_user, 
    initialize,
    get_all_recipes,
    get_all_categories,
    get_top_rated_recipes,
    get_all_reviews
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    featured_recipes = get_all_recipes()[:6]  # Get first 6 recipes as featured
    popular_categories = get_all_categories()[:4]  # Get first 4 categories as popular
    top_rated_recipes = get_top_rated_recipes(limit=3)  # Get top 3 rated recipes
    latest_reviews = get_all_reviews()[:5]  # Get latest 5 reviews
    
    return render_template('index.html', 
                         featured_recipes=featured_recipes,
                         popular_categories=popular_categories,
                         top_rated_recipes=top_rated_recipes,
                         latest_reviews=latest_reviews)

@index_views.route('/about', methods=['GET'])
def about_page():
    return render_template('about.html')

@index_views.route('/categories', methods=['GET'])
def categories_page():
    return render_template('categories.html')