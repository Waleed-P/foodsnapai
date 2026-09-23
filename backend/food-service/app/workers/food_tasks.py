import dramatiq
from app.database import SessionLocal
from app.workers.broker import redis_broker
from app.model.food import FoodItemModel
import os
import app.model
from app.utilities.upload_file import s3_client
from app.utilities.food_prediction import predict_food
dramatiq.set_broker(redis_broker)
db = SessionLocal()
BUCKET_NAME=os.environ["AWS_STORAGE_BUCKET_NAME"]
@dramatiq.actor
def process_food_image(food_item_id):
    print(f"Processing food item {food_item_id}")
    food_item = db.query(FoodItemModel).filter(FoodItemModel.id == food_item_id).first()
    
    if not food_item:
        print(f"Error: Food item with ID {food_item_id} not found in database.")
        return 
        
    object_key = food_item.aws_unique_name
    
    try:
        # Download image from S3
        response = s3_client.get_object(
            Bucket=BUCKET_NAME,
            Key=object_key
        )
        
        # Read the raw bytes from the stream
        image_bytes = response["Body"].read()
        
        # Check if bytes are valid and not empty
        if image_bytes:
            print(f"Success: Image '{object_key}' successfully fetched from S3 bucket!")
        else:
            print(f"Warning: Connection succeeded but image file '{object_key}' is empty.")
            return

    except Exception as e:
        print(f"Error: Failed to fetch image from S3. Details: {e}")
        return

    # Run AI model
    result = predict_food(image_bytes, food_item_id, top_k=1)
    print(result)
    
    # Update database
    # ...