import json
import logging
import os

from openai import OpenAI

logger = logging.getLogger(__name__)


def get_client():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        logger.warning("OPENAI_API_KEY is missing; skipping OpenAI suggestions.")
        return None

    return OpenAI(api_key=api_key)


def get_suggestions(ingredients):
    client = get_client()
    if client is None:
        return []

    prompt = f"""
I have these ingredients: {", ".join(ingredients)}.

Suggest 3 recipes based on them.
Return only valid JSON.
Do not include explanations, markdown, or code fences.
Return recipe titles, ingredients, and steps in Turkish.

JSON format:
{{
  "recipes": [
    {{
      "id": 1,
      "title": "Tarif adi",
      "time": 15,
      "difficulty": "Kolay",
      "ingredients": ["yumurta", "domates"],
      "steps": ["Adim 1", "Adim 2"],
      "score": 2,
      "missing_ingredients": ["biber"],
      "missing_count": 1
    }}
  ]
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a cooking assistant that only returns valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        text = response.choices[0].message.content or ""
    except Exception:
        logger.exception("OpenAI request failed while generating recipe suggestions.")
        return []

    return parse_ai_response(text)


def parse_ai_response(text):
    if not text:
        logger.warning("OpenAI returned an empty response body.")
        return []

    try:
        start = text.find("{")
        end = text.rfind("}") + 1

        if start == -1 or end == 0:
            logger.warning("OpenAI response did not contain a JSON object.")
            return []

        json_text = text[start:end]
        data = json.loads(json_text)
        return data.get("recipes", [])
    except json.JSONDecodeError:
        logger.exception("Failed to decode OpenAI response as JSON.")
        return []
    except Exception:
        logger.exception("Unexpected error while parsing OpenAI response.")
        return []
