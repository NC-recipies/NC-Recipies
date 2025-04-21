from App.models import Recipe, Category, Review, RecipeIngredient, Ingredient
from App.database import db
from datetime import datetime

def create_recipe(title, user_id, category_id=None, description=None, instructions=None, prep_time=None, cook_time=None, servings=None, image_url=None):
    recipe = Recipe(title=title, user_id=user_id, category_id=category_id, description=description, instructions=instructions, prep_time=prep_time, cook_time=cook_time, servings=servings, image_url=image_url)
    db.session.add(recipe)
    db.session.commit()
    return recipe

def get_recipe(id):
    return Recipe.query.get(id)

def get_all_recipes():
    return Recipe.query.all()

def get_all_recipes_json():
    recipes = Recipe.query.all()
    if not recipes:
        return []
    return [recipe.get_json() for recipe in recipes]

def get_top_rated_recipes(limit=3):
    """Get the top rated recipes based on average rating."""
    recipes = Recipe.query.all()
    # Sort recipes by average rating in descending order
    sorted_recipes = sorted(recipes, key=lambda x: x.average_rating, reverse=True)
    return sorted_recipes[:limit]

def update_recipe(id, title=None, description=None, instructions=None, prep_time=None, cook_time=None, servings=None, image_url=None, category_id=None):
    recipe = get_recipe(id)
    if recipe:
        if title is not None:
            recipe.title = title
        if description is not None:
            recipe.description = description
        if instructions is not None:
            recipe.instructions = instructions
        if prep_time is not None:
            recipe.prep_time = prep_time
        if cook_time is not None:
            recipe.cook_time = cook_time
        if servings is not None:
            recipe.servings = servings
        if image_url is not None:
            recipe.image_url = image_url
        if category_id is not None:
            recipe.category_id = category_id
        db.session.commit()
        return recipe
    return None

def delete_recipe(id):
    recipe = get_recipe(id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return True
    return False

def get_recipes_by_user(user_id):
    return Recipe.query.filter_by(user_id=user_id).all()

def get_recipes_by_category(category_id):
    return Recipe.query.filter_by(category_id=category_id).all()

def search_recipes(query):
    return Recipe.query.filter(Recipe.title.ilike(f'%{query}%')).all()

def add_ingredient_to_recipe(recipe_id, ingredient_name, quantity, unit):
    # Check if ingredient exists, if not create it
    ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
    if not ingredient:
        ingredient = Ingredient(name=ingredient_name)
        db.session.add(ingredient)
        db.session.commit()
    
    # Create recipe-ingredient relationship
    recipe_ingredient = RecipeIngredient(
        recipe_id=recipe_id,
        ingredient_id=ingredient.id,
        quantity=quantity,
        unit=unit
    )
    db.session.add(recipe_ingredient)
    db.session.commit()
    return recipe_ingredient

def get_recipe_ingredients(recipe_id):
    return RecipeIngredient.query.filter_by(recipe_id=recipe_id).join(Ingredient).all()

def add_review(recipe_id, user_id, rating, comment=None):
    review = Review(
        recipe_id=recipe_id,
        user_id=user_id,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    db.session.commit()
    return review

def get_recipe_reviews(recipe_id):
    return Review.query.filter_by(recipe_id=recipe_id).all()

def get_recipe_average_rating(recipe_id):
    recipe = get_recipe(recipe_id)
    if recipe:
        return recipe.average_rating
    return 0 