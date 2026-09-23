from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import websockets
import asyncio
import os

router = APIRouter()

FOOD_SERVICE_WS_URL = os.environ["FOOD_SERVICE_WS_URL"]

@router.websocket("/ws/food/{food_id}")
async def proxy_food_websocket(websocket: WebSocket, food_id: int):
    # 1. Origin Check
    client_origin = websocket.headers.get("origin")
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.31.226:3000",
        "*"
    ]
    
    if client_origin in allowed_origins or "*" in allowed_origins:
        await websocket.accept()
    else:
        await websocket.close(code=1008)
        return

    # 2. Proxy connection to downstream Food Service
    target_url = f"{FOOD_SERVICE_WS_URL}/ws/food/{food_id}"

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

            # FIRST TASK TO FINISH CANCELS THE OTHER
            done, pending = await asyncio.wait(
                [
                    asyncio.create_task(forward_backend_to_client()),
                    asyncio.create_task(forward_client_to_backend())
                ],
                return_when=asyncio.FIRST_COMPLETED
            )

            # Clean up pending task
            for task in pending:
                task.cancel()

    except (websockets.exceptions.WebSocketException, ConnectionRefusedError) as e:
        print(f"Failed to connect to Food Service WS: {e}")
        await websocket.close(code=1011)
    except WebSocketDisconnect:
        print("Client disconnected from Gateway WS")
    finally:
        # Ensure client connection closes gracefully
        try:
            await websocket.close()
        except Exception:
            pass