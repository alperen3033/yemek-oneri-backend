from django.contrib.auth import get_user_model
from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from recipes.providers.openai_provider import parse_ai_response
from recipes.serializers import SuggestRequestSerializer

User = get_user_model()


class SuggestRequestSerializerTests(SimpleTestCase):
    def test_accepts_and_normalizes_valid_ingredients(self):
        serializer = SuggestRequestSerializer(
            data={"ingredients": [" domates  ", "yumurta", "taze  sogan "]}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            serializer.validated_data["ingredients"],
            ["domates", "yumurta", "taze sogan"],
        )

    def test_rejects_empty_ingredient_lists(self):
        serializer = SuggestRequestSerializer(data={"ingredients": []})

        self.assertFalse(serializer.is_valid())
        self.assertIn("ingredients", serializer.errors)

    def test_rejects_duplicate_ingredients_case_insensitively(self):
        serializer = SuggestRequestSerializer(
            data={"ingredients": ["Domates", "domates"]}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("ingredients", serializer.errors)

    def test_rejects_ingredients_without_alphanumeric_content(self):
        serializer = SuggestRequestSerializer(data={"ingredients": ["---"]})

        self.assertFalse(serializer.is_valid())
        self.assertIn("ingredients", serializer.errors)


class OpenAIProviderTests(SimpleTestCase):
    def test_parse_ai_response_extracts_embedded_json(self):
        text = 'Here you go {"recipes": [{"id": 1, "title": "Menemen"}]} thanks'

        result = parse_ai_response(text)

        self.assertEqual(result, [{"id": 1, "title": "Menemen"}])

    def test_parse_ai_response_returns_empty_list_for_invalid_json(self):
        result = parse_ai_response("not-json")

        self.assertEqual(result, [])


class AuthApiTests(APITestCase):
    def test_register_creates_user_with_hashed_password(self):
        response = self.client.post(
            reverse("auth-register"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "strongpass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="testuser")
        self.assertNotEqual(user.password, "strongpass123")
        self.assertTrue(user.check_password("strongpass123"))

    def test_login_returns_access_token(self):
        user = User.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="strongpass123",
        )

        response = self.client.post(
            reverse("auth-login"),
            {
                "username": user.username,
                "password": "strongpass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_me_requires_authentication(self):
        response = self.client.get(reverse("auth-me"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_authenticated_user(self):
        user = User.objects.create_user(
            username="meuser",
            email="me@example.com",
            password="strongpass123",
        )
        login_response = self.client.post(
            reverse("auth-login"),
            {
                "username": user.username,
                "password": "strongpass123",
            },
            format="json",
        )
        access_token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(reverse("auth-me"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], user.username)
