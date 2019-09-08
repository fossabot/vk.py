"""
A part of library which represent a main object of VK API.
"""
import asyncio
import logging
import typing
from asyncio import AbstractEventLoop

from aiohttp import ClientSession

from vk.constants import API_LINK
from vk.constants import API_VERSION
from vk.constants import JSON_LIBRARY
from vk.exceptions import APIErrorDispatcher
from vk.methods import API
from vk.utils import ContextInstanceMixin


try:
    import uvloop  # noqa

    uvloop.install()
except ImportError:
    uvloop = None

logger = logging.getLogger(__name__)


class VK(ContextInstanceMixin):
    """
    The main object of VKAPI, have basically methods to access in API.
    """

    def __init__(
        self,
        access_token: str,
        *,
        loop: AbstractEventLoop = None,
        client: ClientSession = None,
    ):

        """

        :param access_token: access token of VK user/community for access to VK methods.
        :param loop: asyncio event loop, uses in Task manager/dispatcher extensions/etc.
        :param client: aiohttp client session
        """
        self.access_token = access_token
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.client = (
            client
            if client is not None and isinstance(client, ClientSession)
            else ClientSession(json_serialize=JSON_LIBRARY.dumps)
        )
        self.api_version = API_VERSION

        self.error_dispatcher = APIErrorDispatcher(self)

        self.__api_object = self.__get_api()
        VK.set_current(self)

    async def _api_request(
        self, method_name: typing.AnyStr, params: dict = None, _raw_mode: bool = False
    ) -> dict:
        """

        :param method_name: method of name when need to call
        :param params: parameters with method
        :param _raw_mode: signal of return 'raw' response, or not (basically, returns response["response"])
        :return:
        """
        if params is None or not isinstance(params, dict):
            params = {}

        params.update({"v": self.api_version, "access_token": self.access_token})
        async with self.client.post(API_LINK + method_name, params=params) as response:
            if response.status == 200:
                json: typing.Dict = await response.json(loads=JSON_LIBRARY.loads)
                logger.debug(f"Method {method_name} called. Response from API: {json}")
                if "error" in json:
                    return await self.error_dispatcher.error_handle(json)

                if _raw_mode:
                    return json

                response = json["response"]
                return response

    async def api_request(self, method_name: str, params: dict = None) -> dict:
        """
        Send api request to VK server
        :param method_name:
        :param params:
        :return:
        """
        return await self._api_request(method_name=method_name, params=params)

    async def execute_api_request(self, code: str) -> dict:
        """
        https://vk.com/dev/execute

        :param code: code for execute. Example: return API.status.get();
        :return:
        """
        return await self.api_request("execute", params={"code": code})

    def __get_api(self) -> API:
        """
        Get API class
        :return:
        """
        api = API(self)
        API.set_current(api)
        return api

    def get_api(self) -> API:
        """
        Get API class
        :return:
        """
        return self.__api_object

    async def close(self) -> None:
        """
        Close aiohttp client session.
        :return:
        """
        if isinstance(self.client, ClientSession) and not self.client.closed:
            await self.client.close()
