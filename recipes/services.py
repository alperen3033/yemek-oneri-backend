def suggest_recipes(user_ingredients, recipes):
    if not user_ingredients:
        return []

    normalized_user_ingredients = {item.strip().lower() for item in user_ingredients if item.strip()}

    scored = []

    for recipe in recipes:
        recipe_ingredients = [ing.strip().lower() for ing in recipe["ingredients"]]

        matched = [ing for ing in recipe_ingredients if ing in normalized_user_ingredients]
        missing = [ing for ing in recipe_ingredients if ing not in normalized_user_ingredients]

        scored.append({
            **recipe,
            "score": len(matched),
            "missing_ingredients": missing,
            "missing_count": len(missing),
        })

    results = [r for r in scored if r["score"] > 0]
    results.sort(key=lambda x: (-x["score"], x["missing_count"]))

    return results[:3]