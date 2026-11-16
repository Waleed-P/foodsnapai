import dramatiq
from dramatiq.brokers.redis import RedisBroker
from app.core.config import settings

# Support both direct Redis URL and host/port connection
if settings.redis_url and settings.redis_url.startswith("redis://"):
    redis_broker = RedisBroker(url=settings.redis_url)
else:
    redis_broker = RedisBroker(
        host=settings.redis_host,
        port=settings.redis_port,
    )

dramatiq.set_broker(redis_broker)
