from .user import create_user
from .category import create_category
from App.database import db
from flask import current_app


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    
    # Create default categories
    default_categories = [
        'Breakfast',
        'Lunch',
        'Dinner',
        'Dessert',
        'Appetizers',
        'Vegetarian',
        'Vegan',
        'Gluten-Free'
    ]
    
    for category_name in default_categories:
        create_category(category_name)
