from rest_framework import serializers


class SuggestRequestSerializer(serializers.Serializer):
    ingredients = serializers.ListField(
        child=serializers.CharField(
            allow_blank=False,
            trim_whitespace=True,
            max_length=50,
        ),
        allow_empty=False,
        min_length=1,
        max_length=20,
    )

    def validate_ingredients(self, value):
        normalized_ingredients = []
        seen_ingredients = set()

        for ingredient in value:
            cleaned = " ".join(ingredient.split())

            if len(cleaned) < 2:
                raise serializers.ValidationError(
                    "Each ingredient must be at least 2 characters long."
                )

            if not any(char.isalnum() for char in cleaned):
                raise serializers.ValidationError(
                    "Each ingredient must contain at least one letter or number."
                )

            ingredient_key = cleaned.casefold()
            if ingredient_key in seen_ingredients:
                raise serializers.ValidationError(
                    "Duplicate ingredients are not allowed."
                )

            seen_ingredients.add(ingredient_key)
            normalized_ingredients.append(cleaned)

        return normalized_ingredients
