from App.models import Review
from App.database import db

def create_review(recipe_id, user_id, rating, comment=None):
    review = Review(
        recipe_id=recipe_id,
        user_id=user_id,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    db.session.commit()
    return review

def get_review(id):
    return Review.query.get(id)

def get_all_reviews():
    return Review.query.all()

def get_all_reviews_json():
    reviews = Review.query.all()
    if not reviews:
        return []
    return [review.get_json() for review in reviews]

def update_review(id, rating=None, comment=None):
    review = get_review(id)
    if review:
        if rating: review.rating = rating
        if comment: review.comment = comment
        db.session.add(review)
        db.session.commit()
        return review
    return None

def delete_review(id):
    review = get_review(id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return True
    return False

def get_reviews_by_user(user_id):
    return Review.query.filter_by(user_id=user_id).all()

def get_reviews_by_recipe(recipe_id):
    return Review.query.filter_by(recipe_id=recipe_id).all()

def get_average_rating(recipe_id):
    reviews = get_reviews_by_recipe(recipe_id)
    if not reviews:
        return 0
    return sum(review.rating for review in reviews) / len(reviews) 