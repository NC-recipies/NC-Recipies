from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, current_app, send_from_directory
from flask_jwt_extended import jwt_required, current_user
import os
from werkzeug.utils import secure_filename

from App.controllers import (
    create_recipe,
    get_recipe,
    get_all_recipes,
    get_all_recipes_json,
    update_recipe,
    delete_recipe,
    get_recipes_by_user,
    get_recipes_by_category,
    search_recipes,
    add_ingredient_to_recipe,
    get_recipe_ingredients,
    add_review,
    get_recipe_reviews,
    get_recipe_average_rating,
    get_all_categories,
    get_all_ingredients
)

recipe_views = Blueprint('recipe_views', __name__, template_folder='../templates')

'''
Page Routes
'''
@recipe_views.route('/recipes', methods=['GET'])
def get_recipe_page():
    recipes = get_all_recipes()
    return render_template('recipes.html', recipes=recipes)

@recipe_views.route('/recipes/<int:id>', methods=['GET'])
def get_recipe_page_by_id(id):
    recipe = get_recipe(id)
    if not recipe:
        flash('Recipe not found')
        return redirect(url_for('recipe_views.get_recipe_page'))
    
    recipe.average_rating = get_recipe_average_rating(id)
    ingredients = get_recipe_ingredients(id)
    reviews = get_recipe_reviews(id)
    
    return render_template('recipe_detail.html', 
                         recipe=recipe, 
                         ingredients=ingredients,
                         reviews=reviews)

@recipe_views.route('/recipes/create', methods=['GET'])
@jwt_required()
def get_create_recipe_page():
    categories = get_all_categories()
    return render_template('create_recipe.html', categories=categories)

@recipe_views.route('/recipes/create', methods=['POST'])
@jwt_required()
def create_recipe_action():
    data = request.form
    image_url = None
    
    if 'image_url' in request.files:
        file = request.files['image_url']
        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            image_url = f"/uploads/{filename}"
    
    recipe = create_recipe(
        title=data['title'],
        description=data['description'],
        instructions=data['instructions'],
        prep_time=int(data['prep_time']),
        cook_time=int(data['cook_time']),
        servings=int(data['servings']),
        user_id=current_user.id,
        category_id=int(data['category_id']),
        image_url=image_url
    )
    
    if recipe:
        # Handle ingredients
        ingredient_names = request.form.getlist('ingredient_names[]')
        ingredient_quantities = request.form.getlist('ingredient_quantities[]')
        ingredient_units = request.form.getlist('ingredient_units[]')
        
        for name, quantity, unit in zip(ingredient_names, ingredient_quantities, ingredient_units):
            if name and quantity and unit:  # Only add if all fields are present
                add_ingredient_to_recipe(
                    recipe_id=recipe.id,
                    ingredient_name=name,
                    quantity=float(quantity),
                    unit=unit
                )
        
        flash('Recipe created successfully!')
        return redirect(url_for('recipe_views.get_recipe_page_by_id', id=recipe.id))
    flash('Error creating recipe')
    return redirect(url_for('recipe_views.get_create_recipe_page'))

@recipe_views.route('/recipes/<int:id>/edit', methods=['GET'])
@jwt_required()
def get_edit_recipe_page(id):
    recipe = get_recipe(id)
    if not recipe or recipe.user_id != current_user.id:
        flash('Recipe not found or unauthorized')
        return redirect(url_for('recipe_views.get_recipe_page'))
    categories = get_all_categories()
    return render_template('edit_recipe.html', recipe=recipe, categories=categories)

@recipe_views.route('/recipes/<int:id>/edit', methods=['POST'])
@jwt_required()
def edit_recipe_action(id):
    recipe = get_recipe(id)
    if not recipe or recipe.user_id != current_user.id:
        flash('Recipe not found or unauthorized')
        return redirect(url_for('recipe_views.get_recipe_page'))
    
    data = request.form
    image_url = recipe.image_url  # Keep existing image by default
    
    if 'image_url' in request.files:
        file = request.files['image_url']
        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            image_url = f"/uploads/{filename}"
    
    recipe = update_recipe(
        id=id,
        title=data.get('title'),
        description=data.get('description'),
        instructions=data.get('instructions'),
        prep_time=int(data.get('prep_time')) if data.get('prep_time') else None,
        cook_time=int(data.get('cook_time')) if data.get('cook_time') else None,
        servings=int(data.get('servings')) if data.get('servings') else None,
        category_id=int(data.get('category_id')) if data.get('category_id') else None,
        image_url=image_url
    )
    if recipe:
        flash('Recipe updated successfully!')
        return redirect(url_for('recipe_views.get_recipe_page_by_id', id=id))
    flash('Error updating recipe')
    return redirect(url_for('recipe_views.get_edit_recipe_page', id=id))

@recipe_views.route('/recipes/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_recipe_action(id):
    recipe = get_recipe(id)
    if not recipe or recipe.user_id != current_user.id:
        flash('Recipe not found or unauthorized')
        return redirect(url_for('recipe_views.get_recipe_page'))
    
    if delete_recipe(id):
        flash('Recipe deleted successfully!')
    else:
        flash('Error deleting recipe')
    return redirect(url_for('recipe_views.get_recipe_page'))

@recipe_views.route('/recipes/search', methods=['GET'])
def search_recipe_page():
    query = request.args.get('query', '')
    recipes = search_recipes(query)
    return render_template('recipes.html', recipes=recipes, search_query=query)

@recipe_views.route('/recipes/<int:id>/reviews/create', methods=['GET'])
@jwt_required()
def get_create_review_page(id):
    recipe = get_recipe(id)
    if not recipe:
        flash('Recipe not found')
        return redirect(url_for('recipe_views.get_recipe_page'))
    return render_template('create_review.html', recipe=recipe)

@recipe_views.route('/recipes/<int:id>/reviews/create', methods=['POST'])
@jwt_required()
def create_review_action(id):
    recipe = get_recipe(id)
    if not recipe:
        flash('Recipe not found')
        return redirect(url_for('recipe_views.get_recipe_page'))
    
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')
    
    if not rating or not comment:
        flash('Please provide both rating and comment')
        return redirect(url_for('recipe_views.get_create_review_page', id=id))
    
    review = add_review(
        recipe_id=id,
        user_id=current_user.id,
        rating=rating,
        comment=comment
    )
    
    if review:
        flash('Review added successfully!')
        return redirect(url_for('recipe_views.get_recipe_page_by_id', id=id))
    
    flash('Error adding review')
    return redirect(url_for('recipe_views.get_create_review_page', id=id))

@recipe_views.route('/recipes/<int:id>/ingredients/add', methods=['GET'])
@jwt_required()
def get_add_ingredient_page(id):
    recipe = get_recipe(id)
    if not recipe or recipe.user_id != current_user.id:
        flash('Recipe not found or unauthorized')
        return redirect(url_for('recipe_views.get_recipe_page'))
    
    ingredients = get_all_ingredients()
    return render_template('add_ingredient.html', recipe=recipe, ingredients=ingredients)

@recipe_views.route('/recipes/<int:id>/ingredients/add', methods=['POST'])
@jwt_required()
def add_ingredient_action(id):
    recipe = get_recipe(id)
    if not recipe or recipe.user_id != current_user.id:
        flash('Recipe not found or unauthorized')
        return redirect(url_for('recipe_views.get_recipe_page'))
    
    ingredient_id = request.form.get('ingredient_id', type=int)
    quantity = request.form.get('quantity', type=float)
    unit = request.form.get('unit')
    
    if not all([ingredient_id, quantity, unit]):
        flash('Please provide all required fields')
        return redirect(url_for('recipe_views.get_add_ingredient_page', id=id))
    
    result = add_ingredient_to_recipe(
        recipe_id=id,
        ingredient_id=ingredient_id,
        quantity=quantity,
        unit=unit
    )
    
    if result:
        flash('Ingredient added successfully!')
    else:
        flash('Error adding ingredient')
    
    return redirect(url_for('recipe_views.get_recipe_page_by_id', id=id))

'''
API Routes
'''
@recipe_views.route('/api/recipes', methods=['GET'])
def get_recipes_api():
    recipes = get_all_recipes_json()
    return jsonify(recipes)

@recipe_views.route('/api/recipes/<int:id>', methods=['GET'])
def get_recipe_api(id):
    recipe = get_recipe(id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    return jsonify(recipe.get_json())

@recipe_views.route('/api/recipes', methods=['POST'])
@jwt_required()
def create_recipe_api():
    data = request.json
    recipe = create_recipe(
        title=data['title'],
        description=data['description'],
        instructions=data['instructions'],
        prep_time=data['prep_time'],
        cook_time=data['cook_time'],
        servings=data['servings'],
        user_id=current_user.id,
        category_id=data['category_id'],
        image_url=data.get('image_url')
    )
    if recipe:
        return jsonify(recipe.get_json()), 201
    return jsonify({'error': 'Error creating recipe'}), 400

@recipe_views.route('/api/recipes/<int:id>', methods=['PUT'])
@jwt_required()
def update_recipe_api(id):
    recipe = get_recipe(id)
    if not recipe or recipe.user_id != current_user.id:
        return jsonify({'error': 'Recipe not found or unauthorized'}), 404
    
    data = request.json
    recipe = update_recipe(
        id=id,
        title=data.get('title'),
        description=data.get('description'),
        instructions=data.get('instructions'),
        prep_time=data.get('prep_time'),
        cook_time=data.get('cook_time'),
        servings=data.get('servings'),
        category_id=data.get('category_id'),
        image_url=data.get('image_url')
    )
    if recipe:
        return jsonify(recipe.get_json())
    return jsonify({'error': 'Error updating recipe'}), 400

@recipe_views.route('/api/recipes/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_recipe_api(id):
    recipe = get_recipe(id)
    if not recipe or recipe.user_id != current_user.id:
        return jsonify({'error': 'Recipe not found or unauthorized'}), 404
    
    if delete_recipe(id):
        return jsonify({'message': 'Recipe deleted successfully'})
    return jsonify({'error': 'Error deleting recipe'}), 400

@recipe_views.route('/api/recipes/search', methods=['GET'])
def search_recipes_api():
    query = request.args.get('query', '')
    recipes = search_recipes(query)
    return jsonify([recipe.get_json() for recipe in recipes])

@recipe_views.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename) 