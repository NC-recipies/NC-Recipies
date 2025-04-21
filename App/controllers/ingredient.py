from App.models import Ingredient, RecipeIngredient
from App.database import db

def create_ingredient(name):
    new_ingredient = Ingredient(name=name)
    db.session.add(new_ingredient)
    db.session.commit()
    return new_ingredient

def get_ingredient(id):
    return Ingredient.query.get(id)

def get_all_ingredients():
    return Ingredient.query.all()

def get_all_ingredients_json():
    ingredients = Ingredient.query.all()
    if not ingredients:
        return []
    return [ingredient.get_json() for ingredient in ingredients]

def update_ingredient(id, name):
    ingredient = get_ingredient(id)
    if ingredient:
        ingredient.name = name
        db.session.add(ingredient)
        db.session.commit()
        return ingredient
    return None

def delete_ingredient(id):
    ingredient = get_ingredient(id)
    if ingredient:
        db.session.delete(ingredient)
        db.session.commit()
        return True
    return False

def get_ingredient_by_name(name):
    return Ingredient.query.filter_by(name=name).first()

def get_ingredients_by_recipe(recipe_id):
    return RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()

def get_ingredients_json_by_recipe(recipe_id):
    recipe_ingredients = get_ingredients_by_recipe(recipe_id)
    if not recipe_ingredients:
        return []
    return [ri.get_json() for ri in recipe_ingredients]

def add_ingredient_to_recipe(recipe_id, ingredient_name, quantity, unit):
    # Check if ingredient exists, if not create it
    ingredient = get_ingredient_by_name(ingredient_name)
    if not ingredient:
        ingredient = create_ingredient(ingredient_name)
    
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

def remove_ingredient_from_recipe(recipe_id, ingredient_id):
    recipe_ingredient = RecipeIngredient.query.filter_by(
        recipe_id=recipe_id,
        ingredient_id=ingredient_id
    ).first()
    
    if recipe_ingredient:
        db.session.delete(recipe_ingredient)
        db.session.commit()
        return True
    return False 