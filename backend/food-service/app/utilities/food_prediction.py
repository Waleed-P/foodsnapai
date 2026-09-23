import io
import json
import numpy as np
from PIL import Image
import tensorflow as tf
from pathlib import Path
from app.database import SessionLocal
from app.model.food import FoodItemModel
from app.utilities.usda_api_call import fetch_usda_nutrients
from app.enum.job_status import JobStatus
import os
import redis
IMG_SIZE = 224
BASE_DIR = Path(__file__).resolve().parent

# Force paths to be absolute relative to this script
MODEL_PATH = str(BASE_DIR / "foodsnap_efficientnet_final.keras")
CLASS_NAMES_PATH = str(BASE_DIR / "class_names.json")
with open(CLASS_NAMES_PATH) as f:
    CLASS_NAMES = json.load(f)
print(f"Model loaded. {len(CLASS_NAMES)} classes ready.")
# Load the model and classes once when the worker process starts
model = tf.keras.models.load_model(MODEL_PATH)
with open(CLASS_NAMES_PATH) as f:
    CLASS_NAMES = json.load(f)
print(f"Model loaded. {len(CLASS_NAMES)} classes ready.")
# r = redis.Redis(host='localhost', port=6379, db=0)
r = redis.Redis(host=os.environ["REDIS_HOST"], port=6379, db=0,decode_responses=True)

def preprocess_image(image_bytes: bytes) -> tf.Tensor:
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img = np.array(img, dtype=np.float32)   
    img = np.expand_dims(img, axis=0)        
    return tf.convert_to_tensor(img)


def predict_food(image_bytes: bytes,food_item_id: int, top_k: int = 1) -> dict:
    
    db = SessionLocal()
    food = db.query(FoodItemModel).filter(FoodItemModel.id == food_item_id).first()
    if not food:
        raise ValueError(f"Food item with ID {food_item_id} not found in database.")
    food.status = JobStatus.PROCESSING
    db.commit()

    if not (1 <= top_k <= len(CLASS_NAMES)):
        raise ValueError(
            f"top_k must be between 1 and {len(CLASS_NAMES)} (total classes)."
        )

    try:
        img = preprocess_image(image_bytes)
    except Exception as e:
        raise RuntimeError(f"Failed to preprocess image: {e}")

    # Run inference
    preds = model.predict(img, verbose=0)[0]
    top_indices = np.argsort(preds)[::-1][:top_k]

    results = [
        {
            "rank": int(i + 1),
            "label": CLASS_NAMES[idx],
            "confidence": round(float(preds[idx]) * 100, 2),
        }
        for i, idx in enumerate(top_indices)
    ]
    
    usda_data = fetch_usda_nutrients(results[0]["label"])
    if usda_data:
        food.name = results[0]["label"]
        food.calories = usda_data["calories"] 
        food.protein = usda_data["protein"]
        food.carbohydrates = usda_data["carbohydrates"]
        food.fats = usda_data["fats"]
        food.status = JobStatus.COMPLETED
        food.confidence = results[0]["confidence"]
    else:
        food.status = JobStatus.FAILED
            
    db.commit()
    result_payload = {
        "status": "completed",
        "food_id": food.id,
        "name": food.name,
        "calories": food.calories,
        "protein": food.protein,
        "carbohydrates": food.carbohydrates,
        "fats": food.fats,
        "confidence":results[0]["confidence"]

    }
    r.publish(f"food_status_{food_item_id}", json.dumps(result_payload))

    # Return a clean dictionary for your worker to update PostgreSQL
    return {
        "top_prediction": results[0]["label"],
        "confidence": results[0]["confidence"],
        "top_k_results": results,
    }