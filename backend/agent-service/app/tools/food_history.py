import logging
from typing import Any, Dict, List
import httpx
from app.core.config import settings

logger = logging.getLogger("agent.tools.food_history")


def get_food_history(user_id: int, date: str, auth_token: str | None = None) -> List[Dict[str, Any]]:
    """
    Fetches food items for a user on a specific date.
    """
    try:
        cookies = {"access_token": auth_token} if auth_token else {}
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

        with httpx.Client(timeout=5.0) as client:
            res = client.get(
                f"{settings.food_service_url}/food/history",
                cookies=cookies,
                headers=headers,
            )
            if res.status_code == 200:
                data = res.json()
                history = data.get("history", [])
                # Filter for the requested date
                matched = [
                    item for item in history
                    if item.get("created_at", "").startswith(date)
                ]
                return matched
    except Exception as e:
        logger.warning(f"Could not reach Food Service for food history: {e}")

    return []
