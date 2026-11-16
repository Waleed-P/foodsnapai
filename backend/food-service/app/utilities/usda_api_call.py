from app.services.spoonacular import fetch_nutrients_for_food

# Legacy function name alias
fetch_usda_nutrients = fetch_nutrients_for_food

__all__ = ["fetch_usda_nutrients", "fetch_nutrients_for_food"]
