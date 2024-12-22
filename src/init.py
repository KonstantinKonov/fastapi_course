from src.connectors.redis_connector import RedisManager
from src.config import settings


redis_manager = RedisManager(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)


from functools import wraps
from src.init import redis_manager
import pickle
def cache(**dec_kwargs):

    cache_ = redis_manager
    expire = dec_kwargs.get('expire')
    def inner(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if await cache_.get(func.__name__) is None:
                print('обращаемся к базе данных или к redis')
                res = await func(*args, **kwargs)
                if expire is not None:
                    await cache_.set(key=func.__name__, value=pickle.dumps(res), expire=expire)
                else:
                    await cache_.set(key=func.__name__, value=pickle.dumps(res))
                return res
            else:
                print('берем из кэша')
                res = await cache_.get(func.__name__)
                return pickle.loads(res)

        return wrapper
    
    return inner