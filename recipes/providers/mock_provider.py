from recipes.mock_data import RECIPES
from recipes.services import suggest_recipes


def get_suggestions(ingredients):
    return suggest_recipes(ingredients, RECIPES)