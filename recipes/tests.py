from django.test import SimpleTestCase

from recipes.providers.openai_provider import parse_ai_response
from recipes.serializers import SuggestRequestSerializer


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
