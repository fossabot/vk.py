from ..dispatcher.extension import BaseExtension
from vk.longpoll import BotLongPoll

import typing
import logging

logger = logging.getLogger(__name__)


class Polling(BaseExtension):
    key = "polling"

    def __init__(self, group_id: int, vk):
        self._longpoll: BotLongPoll = BotLongPoll(group_id, vk)

    async def get_events(self) -> typing.List:
        events = await self._longpoll.listen()
        return events

    async def run(self, dp):
        await self._longpoll._prepare_longpoll()
        logger.info("Polling started!")
        while True:
            events = await self.get_events()
            if events:
                await dp._process_events(events)
