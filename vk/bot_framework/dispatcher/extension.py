from abc import ABC, abstractmethod
from typing import Optional

import typing
import logging
import asyncio

logger = logging.getLogger(__name__)


class AbstractExtension(ABC):
    @abstractmethod
    async def get_events(self) -> typing.List:
        """
        Get events from any resource and returns list of events.
        :return: list of coming events.
        """
        pass

    @abstractmethod
    async def run(self, dp):
        """
        In endless cycle get events from self.get_events function
        and call dispatcher method dp._process_events.
        :param dp: dispatcher
        :return:
        """
        pass


class BaseExtension(AbstractExtension, ABC):
    """
    May be added to extensions with ExtensionsManager and
    used for get events.

    >> extension_manager.run_extension(name=unique_key)
    """

    key = None  # unique key for access to extension


class ExtensionsManager:
    def __init__(self, dp, default_extensions: typing.Dict[str, BaseExtension]):
        self.dp = dp
        self.extensions: typing.Dict[str, BaseExtension] = {}

        self.extensions.update(default_extensions)

    def setup(self, extension: BaseExtension):
        if extension.key is None:
            raise RuntimeError("Unallowed key for extension")

        self.extensions[extension.key] = extension

    async def run_extension(self, name: str, **kwargs):
        """

        :param name: name of extension
        :param kwargs: params which accept extension constructor
        :return:
        """
        extension: Optional[BaseExtension] = self.extensions.get(name)
        if not extension:
            raise RuntimeError("Undefined extension")

        extension = extension(**kwargs)
        self.dp.vk.loop.create_task(extension.run(self.dp))
