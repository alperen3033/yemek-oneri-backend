from django.conf import settings
from django.db import models


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_recipes"
    )
    recipe_title = models.CharField(max_length=255)
    recipe_data = models.JSONField()
    source = models.CharField(max_length=50, default="openai")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.recipe_title}"
