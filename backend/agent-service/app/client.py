import logging
from typing import Any, Optional

try:
    from groq import Groq
except ImportError:
    Groq = None  # type: ignore

from app.core.config import settings

logger = logging.getLogger("agent.client")

_client: Optional[Any] = None


def get_groq_client() -> Optional[Any]:
    global _client
    if _client is None:
        if Groq is None:
            logger.warning("Groq package is not installed. LLM completions disabled.")
            return None
        if not settings.groq_api_key:
            logger.warning("GROQ_API_KEY is not configured.")
        _client = Groq(api_key=settings.groq_api_key or "gsk_placeholder")
    return _client


# Legacy export
client = get_groq_client()

