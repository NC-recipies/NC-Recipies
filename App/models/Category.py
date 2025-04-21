from App.database import db
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recipes = db.relationship('Recipe', back_populates='category', lazy=True)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'recipe_count': len(self.recipes),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }