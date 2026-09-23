import dramatiq
from dramatiq.brokers.redis import RedisBroker
import os
redis_broker = RedisBroker(
    host=os.environ["REDIS_HOST"],
    port=6379
)

dramatiq.set_broker(redis_broker)