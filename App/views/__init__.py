
from .index import index_views
from .auth import auth_views
from .recipe import recipe_views
from .category import category_views
from .review import review_views
from .ingredient import ingredient_views

views = [
    index_views,
    auth_views,
    recipe_views,
    category_views,
    review_views,
    ingredient_views
] 