from django.urls import path
from .views import SuggestRecipesView

urlpatterns = [
    path("suggest/", SuggestRecipesView.as_view(), name="suggest-recipes"),
]