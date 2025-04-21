from App.database import db

class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    
    recipe = db.relationship('Recipe', back_populates='ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipes')

    def __init__(self, recipe_id, ingredient_id, quantity, unit):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.quantity = quantity
        self.unit = unit

    def get_json(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'ingredient_id': self.ingredient_id,
            'ingredient_name': self.ingredient.name,
            'quantity': self.quantity,
            'unit': self.unit
        }

    def __repr__(self):
        return f'<RecipeIngredient {self.ingredient.name}: {self.quantity} {self.unit}>'