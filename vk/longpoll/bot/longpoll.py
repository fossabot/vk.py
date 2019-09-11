import asyncio
import logging

from vk import VK
from vk.constants import JSON_LIBRARY
from vk.utils import mixins

logger = logging.getLogger(__name__)


# https://vk.com/dev/bots_longpoll


class BotLongPoll(mixins.ContextInstanceMixin):
    def __init__(self, group_id: int, vk: VK):
        """

        :param group_id:
        :param vk:
        """
        self.vk = vk
        self.group_id = group_id
        self.server = None
        self.key = None
        self.ts = None

        self.runned = False

        self._update_polling = self._prepare_longpoll

    async def _prepare_longpoll(self):
        """
        :return:
        """
        resp = await self.get_server()
        self.server = resp["server"]
        self.key = resp["key"]
        self.ts = resp["ts"]

        logger.debug(
            f"Prepare polling. Server - {self.server}. Key - {self.key}. TS - {self.ts}"
        )

    async def get_server(self) -> dict:
        """
        Get polling server.
        :return:
        """
        resp = await self.vk.api_request(
            "groups.getLongPollServer", params={"group_id": self.group_id}
        )
        return resp

    async def get_updates(self, key: str, server: str, ts: str) -> dict:
        """
        Get updates from VK.
        :param key:
        :param server:
        :param ts:
        :return:
        """
        async with self.vk.client.post(
            f"{server}?act=a_check&key={key}&ts={ts}&wait=20"
        ) as response:
            resp = await response.json(loads=JSON_LIBRARY.loads)
            logger.debug(f"Response from polling: {resp}")
            return resp

    async def listen(self) -> list:
        """

        :return: list of updates coming from VK
        """
        try:
            updates = await self.get_updates(
                key=self.key, server=self.server, ts=self.ts
            )
            ts = updates.get("ts")
            self.ts = ts if ts else self.ts
            updates_new = updates.get("updates")
            if updates_new:
                logger.debug(f"Get updates from polling: {updates_new}")
                return updates_new
            if updates.get("failed"):
                raise Exception("Update key and server")
        except Exception:  # noqa
            logger.exception("Polling have trouble... Sleeping 1 minute..")
            await self._update_polling()
            await asyncio.sleep(60)

    async def run(self) -> dict:
        """

        :return: last update coming from VK
        """
        if not self.runned:
            await self._prepare_longpoll()
            self.runned = True
            logger.info("Polling started!")
        while True:
            events = await self.listen()
            if events:
                yield events[0]
