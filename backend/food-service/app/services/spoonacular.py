import logging
from typing import Any, Dict, Optional
import httpx
from app.core.config import settings

logger = logging.getLogger("food_service.spoonacular")


def fetch_nutrients_for_food(food_name: str) -> Optional[Dict[str, float]]:
    if not settings.spoonacular_api_key:
        logger.warning("SPOONACULAR_API_KEY is not configured. Skipping nutrient lookup.")
        return None

    cleaned_name = food_name.replace("_", " ").strip()
    params = {
        "apiKey": settings.spoonacular_api_key,
        "query": cleaned_name,
        "addProductInformation": "true",
        "number": 1,
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(settings.spoonacular_url, params=params)
            response.raise_for_status()
            data = response.json()

        products = data.get("products", [])
        if not products:
            return None

        top_product = products[0]
        nutrients = top_product.get("nutrition", {}).get("nutrients", [])

        nutrition_data = {
            "calories": 0.0,
            "protein": 0.0,
            "carbohydrates": 0.0,
            "fats": 0.0,
        }

        for nutrient in nutrients:
            name = nutrient.get("name", "").lower().strip()
            amount = float(nutrient.get("amount", 0.0))

            if name == "calories":
                nutrition_data["calories"] = round(amount, 1)
            elif name == "protein":
                nutrition_data["protein"] = round(amount, 1)
            elif name in ("carbohydrates", "carbs"):
                nutrition_data["carbohydrates"] = round(amount, 1)
            elif name in ("fat", "total fat"):
                nutrition_data["fats"] = round(amount, 1)

        return nutrition_data

    except Exception as e:
        logger.error(f"Error fetching nutrients from Spoonacular for '{food_name}': {e}")
        return None
