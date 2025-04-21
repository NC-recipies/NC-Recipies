from App.database import db
from datetime import datetime

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    recipe = db.relationship('Recipe', backref=db.backref('reviews', lazy=True, cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

    def __init__(self, rating, recipe_id, user_id, comment=None):
        self.rating = rating
        self.recipe_id = recipe_id
        self.user_id = user_id
        self.comment = comment

    def get_json(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'recipe_id': self.recipe_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
        } 