from ..dispatcher.middleware import BaseMiddleware
from ..dispatcher.handler import SkipHandler

import time
import logging

logger = logging.getLogger(__name__)

"""
Built-in middlewares.
"""


class SimpleLoggingMiddleware(BaseMiddleware):
    global LAST_TIME
    LAST_TIME = 0

    async def pre_process_event(self, event, data: dict):
        logger.info(f"New event! Type - {event['type']}")
        global LAST_TIME
        LAST_TIME = time.time()
        return data

    async def post_process_event(self):
        result = time.time() - LAST_TIME
        logger.info(f"Handler handled this in {result:.3f} seconds!")


class OnlyMessagesMiddleware(BaseMiddleware):
    async def pre_process_event(self, event, data: dict) -> dict:
        if event["type"] != "message_new":
            logger.info("New message! Handlers don`t skipped.")
            return data
        else:
            logger.info("Not message. Handlers skipped.")
            raise SkipHandler()

    async def post_process_event(self) -> None:
        pass
