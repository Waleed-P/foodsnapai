import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import redis.asyncio as redis
from app.core.config import settings

logger = logging.getLogger("food_service.ws")
router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/food/{food_id}")
async def websocket_endpoint(websocket: WebSocket, food_id: int):
    await websocket.accept()

    redis_client = redis.from_url(
        settings.redis_url,
        decode_responses=True,
    )
    pubsub = redis_client.pubsub()
    channel = f"food_status_{food_id}"

    try:
        await pubsub.subscribe(channel)
        logger.info(f"Subscribed to {channel} for food_id {food_id}")

        while True:
            # Check for message with 1 second timeout to keep loop alive
            message = await pubsub.get_message(
                ignore_subscribe_messages=True,
                timeout=1.0,
            )
            if message and message.get("data"):
                data = message["data"]
                await websocket.send_text(data)
                logger.info(f"Forwarded status update to client for food_id {food_id}")
                break

            await asyncio.sleep(0.2)

    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected for food_id: {food_id}")
    except Exception as e:
        logger.error(f"WebSocket error for food_id {food_id}: {e}")
    finally:
        try:
            await pubsub.unsubscribe(channel)
            await pubsub.close()
            await redis_client.aclose()
        except Exception:
            pass
