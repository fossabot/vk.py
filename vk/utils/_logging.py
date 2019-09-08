import functools
from timeit import default_timer as timer


def time_logging(logger):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            timer_1 = timer()
            logger.debug(f"Start processing coroutine ({func.__qualname__})...")
            result = await func(*args, **kwargs)
            logger.debug(
                f"Coroutine ({func.__qualname__}) proccessed. Took {round(timer() - timer_1, 2)} seconds."
            )
            return result

        return wrapped

    return wrapper


def args_logging(logger):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            logger.debug(f"Entered to coroutine ({func.__qualname__})...")
            result = await func(*args, **kwargs)
            logger.debug(
                f"Exited from coroutine ({func.__qualname__}) with result: {result}"
            )
            return result

        return wrapped

    return wrapper
