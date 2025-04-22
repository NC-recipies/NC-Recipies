import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Recipe, Category, Review, Ingredient, RecipeIngredient
from App.main import create_app
from App.controllers.initialize import initialize
from App.controllers import (
    create_user, get_all_users_json, get_all_users, initialize,
    # Recipe controllers
    create_recipe, get_all_recipes_json, get_all_recipes,
    # Category controllers
    create_category, get_all_categories_json, get_all_categories,
    # Review controllers
    create_review, get_all_reviews_json, get_all_reviews,
    # Ingredient controllers
    create_ingredient, get_all_ingredients_json, get_all_ingredients
)


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database initialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Recipe Commands
'''

recipe_cli = AppGroup('recipe', help='Recipe object commands')

@recipe_cli.command("create", help="Creates a recipe")
@click.argument("title", default="Test Recipe")
@click.argument("description", default="Test Description")
@click.argument("instructions", default="Test Instructions")
@click.argument("prep_time", default=30)
@click.argument("cook_time", default=60)
@click.argument("servings", default=4)
@click.argument("user_id", default=1)
@click.argument("category_id", default=1)
def create_recipe_command(title, description, instructions, prep_time, cook_time, servings, user_id, category_id):
    create_recipe(title, description, instructions, prep_time, cook_time, servings, user_id, category_id)
    print(f'Recipe "{title}" created!')

@recipe_cli.command("list", help="Lists recipes in the database")
@click.argument("format", default="string")
def list_recipe_command(format):
    if format == 'string':
        print(get_all_recipes())
    else:
        print(get_all_recipes_json())

app.cli.add_command(recipe_cli)

'''
Category Commands
'''

category_cli = AppGroup('category', help='Category object commands')

@category_cli.command("create", help="Creates a category")
@click.argument("name", default="Test Category")
@click.argument("description", default="Test Description")
def create_category_command(name, description):
    create_category(name, description)
    print(f'Category "{name}" created!')

@category_cli.command("list", help="Lists categories in the database")
@click.argument("format", default="string")
def list_category_command(format):
    if format == 'string':
        print(get_all_categories())
    else:
        print(get_all_categories_json())

app.cli.add_command(category_cli)

'''
Review Commands
'''

review_cli = AppGroup('review', help='Review object commands')

@review_cli.command("create", help="Creates a review")
@click.argument("rating", default=5)
@click.argument("comment", default="Test Comment")
@click.argument("user_id", default=1)
@click.argument("recipe_id", default=1)
def create_review_command(rating, comment, user_id, recipe_id):
    create_review(rating, comment, user_id, recipe_id)
    print(f'Review created for recipe {recipe_id}!')

@review_cli.command("list", help="Lists reviews in the database")
@click.argument("format", default="string")
def list_review_command(format):
    if format == 'string':
        print(get_all_reviews())
    else:
        print(get_all_reviews_json())

app.cli.add_command(review_cli)

'''
Ingredient Commands
'''

ingredient_cli = AppGroup('ingredient', help='Ingredient object commands')

@ingredient_cli.command("create", help="Creates an ingredient")
@click.argument("name", default="Test Ingredient")
@click.argument("unit", default="g")
def create_ingredient_command(name, unit):
    create_ingredient(name, unit)
    print(f'Ingredient "{name}" created!')

@ingredient_cli.command("list", help="Lists ingredients in the database")
@click.argument("format", default="string")
def list_ingredient_command(format):
    if format == 'string':
        print(get_all_ingredients())
    else:
        print(get_all_ingredients_json())

app.cli.add_command(ingredient_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("recipe", help="Run Recipe tests")
@click.argument("type", default="all")
def recipe_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "RecipeUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "RecipeIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("category", help="Run Category tests")
@click.argument("type", default="all")
def category_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "CategoryUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "CategoryIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("review", help="Run Review tests")
@click.argument("type", default="all")
def review_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "ReviewUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "ReviewIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("ingredient", help="Run Ingredient tests")
@click.argument("type", default="all")
def ingredient_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "IngredientUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "IngredientIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)