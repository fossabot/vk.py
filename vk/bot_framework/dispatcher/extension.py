import logging
import typing
from abc import ABC
from abc import abstractmethod

T = typing.TypeVar("T")

logger = logging.getLogger(__name__)


class AbstractExtension(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        """
        Method which accept all extension arguments.
        :param kwargs:
        """

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

    >>> extension_manager.run_extension(name=unique_key)
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

    def run_extension(self, name: str, **extension_init_params) -> None:
        """

        :param name: name of extension
        :param extension_init_params: params which accept extension constructor
        :return:
        """
        if typing.TYPE_CHECKING:
            BaseExtension = typing.Type[T]  # noqa

        extension: BaseExtension = self.extensions.get(name)  # noqa
        if not extension:
            raise RuntimeError("Undefined extension")

        extension: BaseExtension = extension(**extension_init_params)
        self.dp.vk.loop.create_task(extension.run(self.dp))
