from App.database import db
from App.models.RecipeIngredients import RecipeIngredient
from datetime import datetime

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    prep_time = db.Column(db.Integer)  # in minutes
    cook_time = db.Column(db.Integer)  # in minutes
    servings = db.Column(db.Integer)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    # Relationships
    user = db.relationship('User', backref=db.backref('recipes', lazy=True))
    category = db.relationship('Category', back_populates='recipes', lazy=True)
    ingredients = db.relationship('RecipeIngredient', back_populates='recipe', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, title, user_id, description=None, instructions=None, prep_time=None, 
                 cook_time=None, servings=None, image_url=None, category_id=None):
        self.title = title
        self.user_id = user_id
        self.description = description
        self.instructions = instructions
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.servings = servings
        self.image_url = image_url
        self.category_id = category_id
        self._average_rating = 0  # Initialize with a default value

    @property #Get the average rating of the recipe.
    def average_rating(self):
        if not hasattr(self, '_average_rating'):
            self._average_rating = 0
        return self._average_rating

    @average_rating.setter #Set the average rating of the recipe.
    def average_rating(self, value):
        self._average_rating = value

    def get_recipe_average_rating(self): #Calculate the average rating of the recipe based on its reviews.
        if not self.reviews:
            return 0
        total_rating = sum(review.rating for review in self.reviews)
        return round(total_rating / len(self.reviews))

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'instructions': self.instructions,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'servings': self.servings,
            'image_url': self.image_url,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'average_rating': self.average_rating
        }
        