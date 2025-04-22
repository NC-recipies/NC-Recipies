from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user

from App.controllers import (
    create_review,
    get_review,
    get_all_reviews,
    get_all_reviews_json,
    update_review,
    delete_review,
    get_reviews_by_user,
    get_reviews_by_recipe,
    get_average_rating,
    get_recipe
)

review_views = Blueprint('review_views', __name__, template_folder='../templates')

'''
Page Routes
'''
@review_views.route('/recipes/<int:recipe_id>/reviews', methods=['GET'])
def get_recipe_reviews_page(recipe_id):
    reviews = get_reviews_by_recipe(recipe_id)
    recipe = get_recipe(recipe_id)
    if recipe:
        recipe.average_rating = get_average_rating(recipe_id)
    return render_template('recipe_reviews.html', reviews=reviews, recipe=recipe)

@review_views.route('/recipes/<int:recipe_id>/reviews/create', methods=['GET'])
@jwt_required()
def get_create_review_page(recipe_id):
    recipe = get_recipe(recipe_id)
    if not recipe:
        flash('Recipe not found')
        return redirect(url_for('recipe_views.get_recipes_page'))
    return render_template('create_review.html', recipe=recipe)

@review_views.route('/recipes/<int:recipe_id>/reviews/create', methods=['POST'])
@jwt_required()
def create_review_action(recipe_id):
    recipe = get_recipe(recipe_id)
    if not recipe:
        flash('Recipe not found')
        return redirect(url_for('recipe_views.get_recipes_page'))
    
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')
    
    if not rating or not comment:
        flash('Please provide both rating and comment')
        return redirect(url_for('review_views.get_create_review_page', recipe_id=recipe_id))
    
    review = create_review(
        recipe_id=recipe_id,
        user_id=current_user.id,
        rating=rating,
        comment=comment
    )
    
    if review:
        flash('Review added successfully!')
        return redirect(url_for('recipe_views.get_recipe_page_by_id', id=recipe_id))
    
    flash('Error adding review')
    return redirect(url_for('review_views.get_create_review_page', recipe_id=recipe_id))

@review_views.route('/reviews/<int:id>/edit', methods=['GET'])
@jwt_required()
def get_edit_review_page(id):
    review = get_review(id)
    if not review:
        flash('Review not found')
        return redirect(url_for('recipe_views.get_recipes_page'))
    
    if review.user_id != current_user.id:
        flash('You can only edit your own reviews')
        return redirect(url_for('recipe_views.get_recipe_page_by_id', id=review.recipe_id))
    
    return render_template('create_review.html', review=review, recipe=review.recipe)

@review_views.route('/reviews/<int:id>/edit', methods=['POST'])
@jwt_required()
def update_review_action(id):
    review = get_review(id)
    if not review:
        flash('Review not found')
        return redirect(url_for('recipe_views.get_recipes_page'))
    
    if review.user_id != current_user.id:
        flash('You can only edit your own reviews')
        return redirect(url_for('recipe_views.get_recipe_page_by_id', id=review.recipe_id))
    
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')
    
    if not rating or not comment:
        flash('Please provide both rating and comment')
        return redirect(url_for('review_views.get_edit_review_page', id=id))
    
    updated_review = update_review(
        id=id,
        rating=rating,
        comment=comment
    )
    
    if updated_review:
        flash('Review updated successfully!')
        return redirect(url_for('recipe_views.get_recipe_page_by_id', id=review.recipe_id))
    
    flash('Error updating review')
    return redirect(url_for('review_views.get_edit_review_page', id=id))

@review_views.route('/reviews/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_review_action(id):
    review = get_review(id)
    if not review:
        flash('Review not found')
        return redirect(url_for('recipe_views.get_recipes_page'))
    
    if review.user_id != current_user.id:
        flash('You can only delete your own reviews')
        return redirect(url_for('recipe_views.get_recipe_page_by_id', id=review.recipe_id))
    
    if delete_review(id):
        flash('Review deleted successfully!')
    else:
        flash('Error deleting review')
    
    return redirect(url_for('recipe_views.get_recipe_page_by_id', id=review.recipe_id))

@review_views.route('/reviews', methods=['GET'])
def get_reviews_page():
    reviews = get_all_reviews()
    return render_template('reviews.html', reviews=reviews)

@review_views.route('/reviews/json', methods=['GET'])
def get_reviews_json():
    reviews = get_all_reviews_json()
    return reviews

@review_views.route('/users/<int:user_id>/reviews', methods=['GET'])
def get_user_reviews_page(user_id):
    reviews = get_reviews_by_user(user_id)
    return render_template('reviews.html', reviews=reviews)

'''
API Routes
'''
@review_views.route('/api/recipes/<int:recipe_id>/reviews', methods=['GET'])
def get_recipe_reviews_api(recipe_id):
    reviews = get_reviews_by_recipe(recipe_id)
    return jsonify([review.get_json() for review in reviews])

@review_views.route('/api/reviews/<int:id>', methods=['GET'])
def get_review_api(id):
    review = get_review(id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    return jsonify(review.get_json())

@review_views.route('/api/recipes/<int:recipe_id>/reviews', methods=['POST'])
@jwt_required()
def create_review_api(recipe_id):
    data = request.json
    review = create_review(
        recipe_id=recipe_id,
        user_id=current_user.id,
        rating=data['rating'],
        comment=data.get('comment')
    )
    if review:
        return jsonify(review.get_json()), 201
    return jsonify({'error': 'Error creating review'}), 400

@review_views.route('/api/reviews/<int:id>', methods=['PUT'])
@jwt_required()
def update_review_api(id):
    review = get_review(id)
    if not review or review.user_id != current_user.id:
        return jsonify({'error': 'Review not found or unauthorized'}), 404
    
    data = request.json
    review = update_review(
        id=id,
        rating=data.get('rating'),
        comment=data.get('comment')
    )
    if review:
        return jsonify(review.get_json())
    return jsonify({'error': 'Error updating review'}), 400

@review_views.route('/api/reviews/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review_api(id):
    review = get_review(id)
    if not review or review.user_id != current_user.id:
        return jsonify({'error': 'Review not found or unauthorized'}), 404
    
    if delete_review(id):
        return jsonify({'message': 'Review deleted successfully'})
    return jsonify({'error': 'Error deleting review'}), 400 