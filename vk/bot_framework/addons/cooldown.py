"""
A simple cooldown util for message handlers.
"""
import functools
import time

from vk.bot_framework.dispatcher.storage import AbstractAsyncExpiredStorage
from vk.types.message import Message

COOLDOWN_MESSAGE = "Please, wait: {cooldown} seconds"  # replace this in own code by:


# set_cooldown_message(message)


def set_cooldown_message(message: str) -> None:
    global COOLDOWN_MESSAGE
    COOLDOWN_MESSAGE = message


def cooldown_handler(
    storage: AbstractAsyncExpiredStorage, cooldown_time=3, for_specify_user=False
):
    """

    :param storage:
    :param cooldown_time: standart cooldown time: 3 seconds
    :param for_specify_user: cooldown for specify user
    :return:
    """

    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            message: Message = args[0]
            if not isinstance(message, Message):
                raise RuntimeError("Cooldown supports only message hanlders")
            if for_specify_user:
                cooldown_name = (
                    f"__coro_tocooldown:{func.__name__}:user:{message.from_id}__"
                )
            else:
                cooldown_name = f"__coro_tocooldown:{func.__name__}__"
            have_cooldown = await storage.exists(cooldown_name)
            if have_cooldown:
                cd = round((await storage.get(cooldown_name)) - time.time(), 3)
                answer = COOLDOWN_MESSAGE.format(cooldown=cd)
                await message.answer(answer)

            else:
                result = await func(*args, **kwargs)
                try:
                    await storage.place(
                        cooldown_name, time.time() + cooldown_time, expire=cooldown_time
                    )
                except RuntimeError:
                    pass
                return result

        return wrapped

    return wrapper
