from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import redis.asyncio as redis
import asyncio
import os

router = APIRouter()

@router.websocket("/ws/food/{food_id}")
async def websocket_endpoint(websocket: WebSocket, food_id: int):
    await websocket.accept()

    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
    redis_client = redis.from_url(REDIS_URL)

    pubsub = redis_client.pubsub()
    await pubsub.subscribe(f"food_status_{food_id}")

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                data = message['data'].decode('utf-8')
                await websocket.send_text(data)
                break  # Completes processing and exits loop
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        print(f"Client disconnected from Food Service WS for food_id: {food_id}")
    finally:
        try:
            await pubsub.unsubscribe(f"food_status_{food_id}")
            await redis_client.aclose()
        except Exception:
            pass