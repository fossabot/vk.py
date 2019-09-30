import logging

from ..dispatcher.handler import SkipHandler
from ..dispatcher.middleware import BaseMiddleware

logger = logging.getLogger(__name__)

"""
Built-in middlewares.
"""


class OnlyMessagesMiddleware(BaseMiddleware):
    meta = {
        "name": "OnlyMessagesMiddleware",
        "description": "A simple middleware for skipping not 'message_new' events.",
        "deprecated": False,
    }

    async def pre_process_event(self, event, data: dict) -> dict:
        if event["type"] != "message_new":
            logger.info("New message! Handlers don`t skipped.")
            return data
        else:
            logger.info("Not message. Handlers skipped.")
            raise SkipHandler()

    async def post_process_event(self) -> None:
        pass
