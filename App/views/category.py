from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user

from App.controllers import (
    create_category,
    get_category,
    get_all_categories,
    get_all_categories_json,
    update_category,
    delete_category,
    get_category_by_name,
    get_recipes_by_category
)

category_views = Blueprint('category_views', __name__, template_folder='../templates')

'''
Page Routes
'''
@category_views.route('/categories', methods=['GET'])
def get_categories_page():
    categories = get_all_categories()
    return render_template('categories.html', categories=categories)

@category_views.route('/categories/<int:id>', methods=['GET'])
def get_category_page(id):
    category = get_category(id)
    if not category:
        flash('Category not found')
        return redirect(url_for('category_views.get_categories_page'))
    recipes = get_recipes_by_category(id)
    return render_template('category_detail.html', category=category, recipes=recipes)

@category_views.route('/categories/create', methods=['GET'])
@jwt_required()
def get_create_category_page():
    return render_template('create_category.html')

@category_views.route('/categories/create', methods=['POST'])
@jwt_required()
def create_category_action():
    data = request.form
    category = create_category(name=data['name'])
    if category:
        flash('Category created successfully!')
        return redirect(url_for('category_views.get_categories_page'))
    flash('Error creating category')
    return redirect(url_for('category_views.get_create_category_page'))

@category_views.route('/categories/<int:id>/edit', methods=['GET'])
@jwt_required()
def get_edit_category_page(id):
    category = get_category(id)
    if not category:
        flash('Category not found')
        return redirect(url_for('category_views.get_categories_page'))
    return render_template('edit_category.html', category=category)

@category_views.route('/categories/<int:id>/edit', methods=['POST'])
@jwt_required()
def edit_category_action(id):
    data = request.form
    category = update_category(id=id, name=data['name'])
    if category:
        flash('Category updated successfully!')
        return redirect(url_for('category_views.get_categories_page'))
    flash('Error updating category')
    return redirect(url_for('category_views.get_edit_category_page', id=id))

@category_views.route('/categories/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_category_action(id):
    if delete_category(id):
        flash('Category deleted successfully!')
    else:
        flash('Error deleting category')
    return redirect(url_for('category_views.get_categories_page'))

'''
API Routes
'''
@category_views.route('/api/categories', methods=['GET'])
def get_categories_api():
    categories = get_all_categories_json()
    return jsonify(categories)

@category_views.route('/api/categories/<int:id>', methods=['GET'])
def get_category_api(id):
    category = get_category(id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(category.get_json())

@category_views.route('/api/categories', methods=['POST'])
@jwt_required()
def create_category_api():
    data = request.json
    category = create_category(name=data['name'])
    if category:
        return jsonify(category.get_json()), 201
    return jsonify({'error': 'Error creating category'}), 400

@category_views.route('/api/categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_category_api(id):
    data = request.json
    category = update_category(id=id, name=data['name'])
    if category:
        return jsonify(category.get_json())
    return jsonify({'error': 'Error updating category'}), 400

@category_views.route('/api/categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category_api(id):
    if delete_category(id):
        return jsonify({'message': 'Category deleted successfully'})
    return jsonify({'error': 'Error deleting category'}), 400 