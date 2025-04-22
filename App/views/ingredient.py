from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user

from App.controllers import (
    create_ingredient,
    get_ingredient,
    get_all_ingredients,
    get_all_ingredients_json,
    update_ingredient,
    delete_ingredient,
    get_ingredient_by_name,
    get_ingredients_by_recipe,
    get_ingredients_json_by_recipe,
    add_ingredient_to_recipe,
    remove_ingredient_from_recipe
)

ingredient_views = Blueprint('ingredient_views', __name__, template_folder='../templates')

'''
Page Routes
'''
@ingredient_views.route('/ingredients', methods=['GET'])
def get_ingredients_page():
    ingredients = get_all_ingredients()
    return render_template('ingredients.html', ingredients=ingredients)

@ingredient_views.route('/ingredients/<int:id>', methods=['GET'])
def get_ingredient_page(id):
    ingredient = get_ingredient(id)
    if not ingredient:
        flash('Ingredient not found')
        return redirect(url_for('ingredient_views.get_ingredients_page'))
    return render_template('ingredient_detail.html', ingredient=ingredient)

@ingredient_views.route('/ingredients/create', methods=['GET'])
@jwt_required()
def get_create_ingredient_page():
    return render_template('create_ingredient.html')

@ingredient_views.route('/ingredients/create', methods=['POST'])
@jwt_required()
def create_ingredient_action():
    data = request.form
    ingredient = create_ingredient(
        name=data['name'],
        description=data.get('description'),
        unit=data.get('unit')
    )
    if ingredient:
        flash('Ingredient created successfully!')
        return redirect(url_for('ingredient_views.get_ingredient_page', id=ingredient.id))
    flash('Error creating ingredient')
    return redirect(url_for('ingredient_views.get_create_ingredient_page'))

@ingredient_views.route('/ingredients/<int:id>/edit', methods=['GET'])
@jwt_required()
def get_edit_ingredient_page(id):
    ingredient = get_ingredient(id)
    if not ingredient:
        flash('Ingredient not found')
        return redirect(url_for('ingredient_views.get_ingredients_page'))
    return render_template('edit_ingredient.html', ingredient=ingredient)

@ingredient_views.route('/ingredients/<int:id>/edit', methods=['POST'])
@jwt_required()
def edit_ingredient_action(id):
    ingredient = get_ingredient(id)
    if not ingredient:
        flash('Ingredient not found')
        return redirect(url_for('ingredient_views.get_ingredients_page'))
    
    data = request.form
    ingredient = update_ingredient(
        id=id,
        name=data.get('name'),
        description=data.get('description'),
        unit=data.get('unit')
    )
    if ingredient:
        flash('Ingredient updated successfully!')
        return redirect(url_for('ingredient_views.get_ingredient_page', id=id))
    flash('Error updating ingredient')
    return redirect(url_for('ingredient_views.get_edit_ingredient_page', id=id))

@ingredient_views.route('/ingredients/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_ingredient_action(id):
    ingredient = get_ingredient(id)
    if not ingredient:
        flash('Ingredient not found')
        return redirect(url_for('ingredient_views.get_ingredients_page'))
    
    if delete_ingredient(id):
        flash('Ingredient deleted successfully!')
    else:
        flash('Error deleting ingredient')
    return redirect(url_for('ingredient_views.get_ingredients_page'))

@ingredient_views.route('/recipes/<int:recipe_id>/ingredients', methods=['GET'])
def get_recipe_ingredients_page(recipe_id):
    ingredients = get_ingredients_by_recipe(recipe_id)
    return render_template('recipe_ingredients.html', ingredients=ingredients, recipe_id=recipe_id)

@ingredient_views.route('/recipes/<int:recipe_id>/ingredients/add', methods=['GET'])
@jwt_required()
def get_add_ingredient_to_recipe_page(recipe_id):
    ingredients = get_all_ingredients()
    return render_template('add_ingredient_to_recipe.html', ingredients=ingredients, recipe_id=recipe_id)

@ingredient_views.route('/recipes/<int:recipe_id>/ingredients/add', methods=['POST'])
@jwt_required()
def add_ingredient_to_recipe_action(recipe_id):
    data = request.form
    name = data.get('name')
    quantity = float(data.get('quantity'))
    unit = data.get('unit')
    
    # First, create or get the ingredient
    ingredient = get_ingredient_by_name(name)
    if not ingredient:
        ingredient = create_ingredient(
            name=name,
            unit=unit  # Use the provided unit as the default unit
        )
        if not ingredient:
            flash('Error creating ingredient')
            return redirect(url_for('ingredient_views.get_add_ingredient_to_recipe_page', recipe_id=recipe_id))
    
    # Then add it to the recipe
    result = add_ingredient_to_recipe(
        recipe_id=recipe_id,
        ingredient_id=ingredient.id,
        quantity=quantity,
        unit=unit
    )
    
    if result:
        flash('Ingredient added to recipe successfully!')
    else:
        flash('Error adding ingredient to recipe')
    
    return redirect(url_for('ingredient_views.get_recipe_ingredients_page', recipe_id=recipe_id))

@ingredient_views.route('/recipes/<int:recipe_id>/ingredients/<int:ingredient_id>/remove', methods=['POST'])
@jwt_required()
def remove_ingredient_from_recipe_action(recipe_id, ingredient_id):
    if remove_ingredient_from_recipe(recipe_id, ingredient_id):
        flash('Ingredient removed from recipe successfully!')
    else:
        flash('Error removing ingredient from recipe')
    return redirect(url_for('ingredient_views.get_recipe_ingredients_page', recipe_id=recipe_id))

@ingredient_views.route('/ingredients/search', methods=['GET'])
def search_ingredients():
    name = request.args.get('name', '')
    if name:
        ingredient = get_ingredient_by_name(name)
        if ingredient:
            return redirect(url_for('ingredient_views.get_ingredient_page', id=ingredient.id))
        flash(f'No ingredient found with name "{name}"')
    return redirect(url_for('ingredient_views.get_ingredients_page'))

'''
API Routes
'''
@ingredient_views.route('/api/ingredients', methods=['GET'])
def get_ingredients_api():
    ingredients = get_all_ingredients_json()
    return jsonify(ingredients)

@ingredient_views.route('/api/ingredients/<int:id>', methods=['GET'])
def get_ingredient_api(id):
    ingredient = get_ingredient(id)
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    return jsonify(ingredient.get_json())

@ingredient_views.route('/api/ingredients', methods=['POST'])
@jwt_required()
def create_ingredient_api():
    data = request.json
    ingredient = create_ingredient(
        name=data['name'],
        description=data.get('description'),
        unit=data.get('unit')
    )
    if ingredient:
        return jsonify(ingredient.get_json()), 201
    return jsonify({'error': 'Error creating ingredient'}), 400

@ingredient_views.route('/api/ingredients/<int:id>', methods=['PUT'])
@jwt_required()
def update_ingredient_api(id):
    ingredient = get_ingredient(id)
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    
    data = request.json
    ingredient = update_ingredient(
        id=id,
        name=data.get('name'),
        description=data.get('description'),
        unit=data.get('unit')
    )
    if ingredient:
        return jsonify(ingredient.get_json())
    return jsonify({'error': 'Error updating ingredient'}), 400

@ingredient_views.route('/api/ingredients/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ingredient_api(id):
    ingredient = get_ingredient(id)
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    
    if delete_ingredient(id):
        return jsonify({'message': 'Ingredient deleted successfully'})
    return jsonify({'error': 'Error deleting ingredient'}), 400

@ingredient_views.route('/api/recipes/<int:recipe_id>/ingredients', methods=['GET'])
def get_recipe_ingredients_api(recipe_id):
    ingredients = get_ingredients_json_by_recipe(recipe_id)
    return jsonify(ingredients)

@ingredient_views.route('/api/recipes/<int:recipe_id>/ingredients', methods=['POST'])
@jwt_required()
def add_ingredient_to_recipe_api(recipe_id):
    data = request.json
    result = add_ingredient_to_recipe(
        recipe_id=recipe_id,
        ingredient_id=data['ingredient_id'],
        quantity=data['quantity'],
        unit=data['unit']
    )
    if result:
        return jsonify(result.get_json()), 201
    return jsonify({'error': 'Error adding ingredient to recipe'}), 400

@ingredient_views.route('/api/recipes/<int:recipe_id>/ingredients/<int:ingredient_id>', methods=['DELETE'])
@jwt_required()
def remove_ingredient_from_recipe_api(recipe_id, ingredient_id):
    if remove_ingredient_from_recipe(recipe_id, ingredient_id):
        return jsonify({'message': 'Ingredient removed from recipe successfully'})
    return jsonify({'error': 'Error removing ingredient from recipe'}), 400

@ingredient_views.route('/api/recipes/<int:recipe_id>/ingredients/json', methods=['GET'])
def get_recipe_ingredients_json(recipe_id):
    ingredients = get_ingredients_json_by_recipe(recipe_id)
    return jsonify(ingredients) 