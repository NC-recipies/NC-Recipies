from App.database import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    recipes = db.relationship('RecipeIngredient', back_populates='ingredient')

    def __init__(self, name):
        self.name = name

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name
        }
        