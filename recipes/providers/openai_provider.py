import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_suggestions(ingredients):
    prompt = f"""
Elimde şu malzemeler var: {", ".join(ingredients)}.

Bu malzemelere göre 3 yemek öner.

SADECE geçerli JSON dön.
Açıklama yazma.
Markdown kullanma.
Kod bloğu kullanma.

JSON formatı şu olsun:
{{
  "recipes": [
    {{
      "id": 1,
      "title": "Tarif adı",
      "time": 15,
      "difficulty": "Kolay",
      "ingredients": ["yumurta", "domates"],
      "steps": ["Adım 1", "Adım 2"],
      "score": 2,
      "missing_ingredients": ["biber"],
      "missing_count": 1
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a cooking assistant that only returns valid JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    text = response.choices[0].message.content
    return parse_ai_response(text)


def parse_ai_response(text):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1

        if start == -1 or end == 0:
            return []

        json_text = text[start:end]
        data = json.loads(json_text)
        return data.get("recipes", [])
    except Exception as e:
        print("OpenAI parse error:", e)
        return []