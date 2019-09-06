import functools
from timeit import default_timer as timer


def time_logging(logger):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args):
            timer_1 = timer()
            logger.debug("Start processing coroutine...")
            result = await func(*args)
            logger.debug(f"Proccessed. Took {timer() - timer_1} seconds.")
            return result

        return wrapped

    return wrapper
