from django.contrib import admin
from django.urls import path, include

from recipes.views import (
    FavoriteRecipeDeleteView,
    FavoriteRecipeListCreateView,
    LoginView,
    MeView,
    RegisterView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/register/", RegisterView.as_view(), name="auth-register"),
    path("api/auth/login/", LoginView.as_view(), name="auth-login"),
    path("api/auth/me/", MeView.as_view(), name="auth-me"),
    path("api/favorites/", FavoriteRecipeListCreateView.as_view(), name="favorite-list-create"),
    path("api/recipes/", include("recipes.urls")),
    path("api/favorites/<int:favorite_id>/", FavoriteRecipeDeleteView.as_view(), name="favorite-delete"),
]