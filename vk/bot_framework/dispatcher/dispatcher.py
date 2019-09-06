import logging
import typing

from .extension import BaseExtension
from .extension import ExtensionsManager
from .handler import Handler
from .middleware import MiddlewareManager
from .rule import RuleFactory
from .storage import AbstractStorage
from vk import VK
from vk.constants import default_extensions
from vk.constants import default_rules
from vk.types import BotEvent as Event
from vk.utils import ContextInstanceMixin
from vk.utils import time_logging
from vk.utils.get_event import get_event_object

logger = logging.getLogger(__name__)


class Dispatcher(ContextInstanceMixin):
    def __init__(self, vk: VK, group_id: int):
        self.vk: VK = vk
        self.group_id: int = group_id
        self._hanlders: typing.List[Handler] = []

        self._middleware_manager: MiddlewareManager = MiddlewareManager(self)
        self._rule_factory: RuleFactory = RuleFactory(default_rules())
        self._extensions_manager: ExtensionsManager = ExtensionsManager(
            self, default_extensions()
        )

        self._storage: AbstractStorage = None

    @property
    def storage(self):
        if not self._storage:
            raise RuntimeError("Storage not setuped.")
        return self._storage

    @storage.setter
    def storage(self, storage: AbstractStorage):
        self._storage = storage

    def _register_handler(self, handler: Handler):
        """
        Append handler to handlers list
        :param handler:
        :return:
        """
        self._hanlders.append(handler)
        logger.debug(f"Handler '{handler.handler.__name__}' successfully added!")

    def register_message_handler(self, coro: typing.Callable, rules: typing.List):
        """
        Register message handler

        >>> dp.register_message_handler(my_handler, [])

        :param coro:
        :param rules:
        :return:
        """
        event_type = Event.MESSAGE_NEW
        handler = Handler(event_type, coro, rules)
        self._register_handler(handler)

    def message_handler(self, *rules, **named_rules):
        """
        Register message handler with decorator.

        >>> @dp.message_handler(text="hello")
        >>> async def my_func(msg: types.Message, data: dict):
        >>>    print(msg)


        :param rules:
        :param named_rules:
        :return:
        """

        def decorator(coro: typing.Callable):
            nonlocal named_rules
            named_rules = self._rule_factory.get_rules(named_rules)
            self.register_message_handler(coro, named_rules + list(rules))
            return coro

        return decorator

    def register_event_handler(
        self, coro: typing.Callable, event_type: Event, rules: typing.List
    ):
        """
        Register event handler.

        >>> dp.register_event_hanlder(my_handler, Event.WallReplyNew, [])

        :param coro:
        :param event_type:
        :param rules:
        :return:
        """
        handler = Handler(event_type, coro, rules=rules)
        self._register_handler(handler)

    def event_handler(self, event_type: Event, *rules, **named_rules):
        """
        Register event handler with decorator.

        >>> @dp.event_handler(Event.WALL_REPLY_NEW)
        >>> async def my_func(event: eventobj.WallReplyNew, data: dict):
        >>>    print(event)

        :param event_type:
        :param rules:
        :param named_rules:
        :return:
        """

        def decorator(coro: typing.Callable):
            nonlocal named_rules
            named_rules = self._rule_factory.get_rules(named_rules)
            self.register_event_handler(coro, event_type, named_rules + list(rules))
            return coro

        return decorator

    def setup_middleware(self, middleware):
        """
        Add middleware to middlewares list with middleware manager.
        :param middleware:
        :return:
        """
        self._middleware_manager.setup(middleware)

    def setup_rule(self, rule):
        """
        Add named rule to named rules list with rule factory.
        :param rule:
        :return:
        """
        self._rule_factory.setup(rule)

    def setup_extension(self, extension: BaseExtension):
        """
        Add extension to extensions list with extension manager.
        :param extension:
        :return:
        """
        self._extensions_manager.setup(extension)

    def run_extension(self, name: str, **extension_init_params):
        """
        Run extensions with extension manager.
        :param name: name of extension
        :param extension_init_params: params which accept extension constructor
        :return:
        """
        self._extensions_manager.run_extension(name, **extension_init_params)

    @time_logging(logger)
    async def _process_event(self, event: dict):
        """
        Handle 1 event coming from VK.
        :param event:
        :return:
        """
        data = {}  # dict for transfer data from middlewares to handlers and filters.
        # examples/bot_framework/simple_middleware.py

        _skip_handler, data = await self._middleware_manager.trigger_pre_process_middlewares(
            event, data
        )  # trigger pre_process_event funcs in middlewares.
        # returns service value '_skip_handler' and data variable (check upper).

        if (
            not _skip_handler
        ):  # if middlewares don`t skip this handler, dispatcher be check
            # rules and execute handlers.
            ev = get_event_object(event)  # get event pydantic model.
            for handler in self._hanlders:  # check handlers
                if (
                    handler.event_type.value == ev.type
                ):  # if hanlder type is equal event pydantic model.
                    try:
                        result = await handler.execute_handler(
                            ev.object, data
                        )  # if execute hanlder func
                        # return non-False value, other handlers doesn`t be executed.
                        if result:
                            break
                    except Exception:  # noqa
                        logger.exception(
                            f"Error in handler ({handler.handler.__name__}):"
                        )

        await self._middleware_manager.trigger_post_process_middlewares()
        # trigger post_process_event funcs in middlewares.

    async def _process_events(self, events: typing.List[dict]):
        """
        Process events coming from extensions.
        :param events: list of events.
        :return:
        """
        for event in events:
            self.vk.loop.create_task(self._process_event(event))

    def run_polling(self):
        self._extensions_manager.run_extension(
            "polling", group_id=self.group_id, vk=self.vk
        )
