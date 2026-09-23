import os
import httpx
SPOONACULAR_API_KEY = os.environ["SPOONACULAR_API_KEY"]
SPOONACULAR_URL = os.environ["SPOONACULAR_URL"]


def fetch_usda_nutrients(food_name: str):
    print("From Spoonacular API, food is:", food_name)
    
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "query": food_name,               
        "addProductInformation": "true", 
        "number": 1                      
    }
    
    try:
        with httpx.Client() as client:
            response = client.get(SPOONACULAR_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
        products = data.get("products", [])
        if not products:
            return None
            
        top_product = products[0]
        nutrients = top_product.get("nutrition", {}).get("nutrients", [])
        
        nutrition_data = {"calories": 0.0, "protein": 0.0, "carbohydrates": 0.0, "fats": 0.0}
        
        for nutrient in nutrients:
            name = nutrient.get("name", "").lower().strip()
            value = nutrient.get("amount", 0.0)
    
            if name == "calories":
                nutrition_data["calories"] = value
            elif name == "protein":
                nutrition_data["protein"] = value
            elif name == "carbohydrates" or name == "carbs":
                nutrition_data["carbohydrates"] = value
            elif name == "fat":
                nutrition_data["fats"] = value

        return nutrition_data

    except Exception as e:
        print(f"Error fetching data from Spoonacular: {e}")
        return None