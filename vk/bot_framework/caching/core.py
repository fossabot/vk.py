import functools

from .cached_object import CachedResponse
from vk.bot_framework import Dispatcher
from vk.bot_framework.storages import RedisStorage
from vk.constants import JSON_LIBRARY
from vk.types.events.community.event import MessageNew

"""
Now supporting only RedisStorage.
"""


def cached_handler(storage: RedisStorage, expire=10, for_specify_user=False):
    """
    Standart caching time: 10 seconds
    :param for_specify_user: cache this for specify users
    :param storage:
    :param expire:
    :return:
    """

    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            message = MessageNew.get_current()
            if for_specify_user:
                cache_name = (
                    f"__coro_tocache:{func.__name__}:user:{message.object.from_id}__"
                )
            else:
                cache_name = f"__coro_tocache:{func.__name__}__"
            in_cache = await storage.exists(cache_name)
            if in_cache:
                cache = await storage.get(cache_name)
                cache = JSON_LIBRARY.loads(cache)
                params: dict = cache["method_params"]
                params.update(
                    {
                        "peer_id": message.object.peer_id,
                        "from_id": message.object.from_id,
                    }
                )
                return await Dispatcher.get_current().vk.api_request(
                    cache["method_name"], params
                )
            else:
                result = await func(*args, **kwargs)
                if not isinstance(result, CachedResponse):
                    raise ValueError(
                        "Unexpected Response. Please return 'CachedResponse' for use this decorator"
                    )

                await storage.place(
                    cache_name, JSON_LIBRARY.dumps(result.dict()), expire=expire
                )
                return result

        return wrapped

    return wrapper
