from django.conf import settings
from recipes.providers import mock_provider, openai_provider


def get_recipe_suggestions(ingredients):
    if settings.AI_PROVIDER == "openai":
        return openai_provider.get_suggestions(ingredients)

    return mock_provider.get_suggestions(ingredients)