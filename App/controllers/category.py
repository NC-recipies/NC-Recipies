from App.models import Category
from App.database import db

def create_category(name):
    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    return new_category

def get_category(id):
    return Category.query.get(id)

def get_all_categories():
    return Category.query.all()

def get_all_categories_json():
    categories = Category.query.all()
    if not categories:
        return []
    return [category.get_json() for category in categories]

def update_category(id, name):
    category = get_category(id)
    if category:
        category.name = name
        db.session.add(category)
        db.session.commit()
        return category
    return None

def delete_category(id):
    category = get_category(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return True
    return False

def get_category_by_name(name):
    return Category.query.filter_by(name=name).first() 