import json
import logging
import dramatiq
import redis
from sqlalchemy import select
from app.core.config import settings
from app.core.database import SessionLocal
from app.enums.job_status import JobStatus
from app.models.food import FoodItemModel
from app.services.ml import predict_food_labels
from app.services.s3 import download_file_from_s3
from app.services.spoonacular import fetch_nutrients_for_food
from app.workers.broker import redis_broker

logger = logging.getLogger("food_service.worker")
dramatiq.set_broker(redis_broker)


def _get_redis_sync_client():
    if settings.redis_url and settings.redis_url.startswith("redis://"):
        return redis.from_url(settings.redis_url, decode_responses=True)
    return redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        decode_responses=True,
    )


@dramatiq.actor(max_retries=3)
def process_food_image(food_item_id: int):
    logger.info(f"Processing food item ID: {food_item_id}")
    r_client = _get_redis_sync_client()

    with SessionLocal() as db:
        food_item = db.scalar(
            select(FoodItemModel).where(FoodItemModel.id == food_item_id)
        )
        if not food_item:
            logger.error(f"Food item {food_item_id} not found in database.")
            return

        food_item.status = JobStatus.PROCESSING
        db.commit()

        # 1. Download image from S3
        try:
            image_bytes = download_file_from_s3(food_item.aws_unique_name)
            if not image_bytes:
                raise ValueError("Downloaded image payload is empty.")
        except Exception as e:
            logger.error(f"Failed to fetch image from S3: {e}")
            food_item.status = JobStatus.FAILED
            db.commit()
            fail_payload = {
                "status": "failed",
                "food_id": food_item.id,
                "error": "Failed to retrieve image from storage",
            }
            r_client.publish(f"food_status_{food_item_id}", json.dumps(fail_payload))
            return

        # 2. Run Machine Learning inference
        try:
            predictions = predict_food_labels(image_bytes, top_k=1)
            top_prediction = predictions[0]
            food_name = top_prediction["label"]
            confidence = top_prediction["confidence"]
        except Exception as e:
            logger.error(f"ML inference error: {e}")
            food_item.status = JobStatus.FAILED
            db.commit()
            fail_payload = {
                "status": "failed",
                "food_id": food_item.id,
                "error": "Failed to analyze food image with AI",
            }
            r_client.publish(f"food_status_{food_item_id}", json.dumps(fail_payload))
            return

        # 3. Fetch nutritional information
        nutrients = fetch_nutrients_for_food(food_name)
        food_item.name = food_name.replace("_", " ").title()
        food_item.confidence = confidence

        if nutrients:
            food_item.calories = nutrients["calories"]
            food_item.protein = nutrients["protein"]
            food_item.carbohydrates = nutrients["carbohydrates"]
            food_item.fats = nutrients["fats"]
            food_item.status = JobStatus.COMPLETED
        else:
            # Prediction succeeded, nutrition data wasn't matched (or API key not present)
            food_item.status = JobStatus.COMPLETED

        db.commit()

        # 4. Publish real-time status to Redis pub/sub for WebSocket client
        result_payload = {
            "status": food_item.status.value,
            "food_id": food_item.id,
            "name": food_item.name,
            "calories": food_item.calories,
            "protein": food_item.protein,
            "carbohydrates": food_item.carbohydrates,
            "fats": food_item.fats,
            "confidence": food_item.confidence,
        }
        r_client.publish(f"food_status_{food_item_id}", json.dumps(result_payload))
        logger.info(f"Processed food item {food_item_id} successfully: {food_item.name}")
