import logging
from typing import Any, Dict
import httpx
from app.core.config import settings

logger = logging.getLogger("agent.tools.nutrition_history")


def get_nutrition_history(
    user_id: int,
    start_date: str,
    end_date: str,
    auth_token: str | None = None,
) -> Dict[str, Any]:
    """
    Fetches daily aggregated nutrition for a user between two dates.
    """
    try:
        cookies = {"access_token": auth_token} if auth_token else {}
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

        with httpx.Client(timeout=5.0) as client:
            res = client.get(
                f"{settings.food_service_url}/food/nutrition/history",
                params={"start_date": start_date, "end_date": end_date},
                cookies=cookies,
                headers=headers,
            )
            if res.status_code == 200:
                return res.json()
    except Exception as e:
        logger.warning(f"Could not reach Food Service for nutrition history: {e}")

    return {
        "start_date": start_date,
        "end_date": end_date,
        "data": [],
    }
