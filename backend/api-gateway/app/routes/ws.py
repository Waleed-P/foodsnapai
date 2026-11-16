import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import websockets
from app.core.config import settings

logger = logging.getLogger("gateway.ws")
router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/food/{food_id}")
async def proxy_food_websocket(websocket: WebSocket, food_id: int):
    # Origin check
    client_origin = websocket.headers.get("origin")
    allowed_origins = set(settings.cors_origins + ["http://localhost:3000", "http://127.0.0.1:3000"])

    if client_origin and client_origin not in allowed_origins:
        logger.warning(f"Rejected WS connection from disallowed origin: {client_origin}")
        await websocket.close(code=1008)
        return

    await websocket.accept()

    target_url = f"{settings.food_service_ws_url}/ws/food/{food_id}"
    logger.info(f"Connecting WebSocket proxy to downstream: {target_url}")

    try:
        async with websockets.connect(target_url) as backend_ws:
            async def forward_backend_to_client():
                try:
                    async for message in backend_ws:
                        await websocket.send_text(message)
                except Exception:
                    pass

            async def forward_client_to_backend():
                try:
                    while True:
                        data = await websocket.receive_text()
                        await backend_ws.send(data)
                except (WebSocketDisconnect, Exception):
                    pass

            done, pending = await asyncio.wait(
                [
                    asyncio.create_task(forward_backend_to_client()),
                    asyncio.create_task(forward_client_to_backend()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )

            for task in pending:
                task.cancel()

    except (websockets.exceptions.WebSocketException, ConnectionRefusedError) as e:
        logger.error(f"Failed to connect to Food Service WS at {target_url}: {e}")
        try:
            await websocket.close(code=1011)
        except Exception:
            pass
    except WebSocketDisconnect:
        logger.info(f"Client disconnected from Gateway WS for food_id {food_id}")
    finally:
        try:
            await websocket.close()
        except Exception:
            pass
