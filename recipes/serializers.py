from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = authenticate(
            username=attrs.get("username"),
            password=attrs.get("password"),
        )

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        attrs["user"] = user
        return attrs
