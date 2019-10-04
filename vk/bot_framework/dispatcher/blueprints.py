"""
A simple abstraction for build largest bots and sharing rules beetwen handlers.

Example usecase:

    You have a simple bot with admin and user commands[handlers],
    what to limit access to admin commands[handlers] you create a simple rule[named rule, rule] for passing him
    in message_handler decorator. If you have a really big count of commands, you need write this:

    .. code-block:: python3
        @dp.message_handler(is_admin=True)
        async def some(msg, data):
            ...

    repeatedly. We appreciate your time and we create blueprints for this simple cases.

    But! If you have a largest bot with a lof of handlers, you need a simple, and more powerful
    tool for register handlers.
    Blueprints registering looks like that:

    .. code-block:: python3
        blueprint = Blueprint(...)
        dp.setup_blueprint(blueprint)

    It`s easy!

"""
import typing
from abc import ABC
from abc import abstractmethod
from collections import namedtuple

from vk import types
from vk.bot_framework.dispatcher.rule import BaseRule
from vk.types import BotEvent as Event

HandlerInBlueprint = namedtuple(
    "HandlerInBlueprint", "coro event_type rules named_rules meta"
)


class AbstractBlueprint(ABC):
    @abstractmethod
    def message_handler(
        self,
        *rules: typing.Tuple[typing.Type[BaseRule]],
        **named_rules: typing.Dict[str, typing.Any],
    ):
        """
        Register a message handler in blueprint.
        :param rules:
        :param named_rules:
        :return:
        """

    @abstractmethod
    def event_handler(
        self,
        event_type: Event,
        *rules: typing.Tuple[typing.Type[BaseRule]],
        **named_rules: typing.Dict[str, typing.Any],
    ):
        """
        Register a event handler in blueprint.
        :param event_type:
        :param rules:
        :param named_rules:
        :return:
        """


class Blueprint(AbstractBlueprint):
    def __init__(self, *rules: typing.Tuple[BaseRule], **named_rules):
        self.default_rules = rules
        self.default_named_rules = named_rules

        self._handlers: typing.List[HandlerInBlueprint] = []

        self._name = "A yet another blueprint"
        self._description = "Hm..."
        self._meta: dict = {}  # storage a any information here

    @property
    def handlers(self):
        return self._handlers

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def meta(self) -> dict:
        return self._meta

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @description.setter
    def description(self, new_description: str):
        self._description = new_description

    @meta.setter
    def meta(self, new_meta: dict):
        self._meta = new_meta

    def get_handler(self, handler_coro: typing.Callable):
        """
        Get handler object by handler coroutine.
        :param handler_coro:
        :return:
        """
        for handler in self.handlers:
            if handler.coro is handler_coro:
                return handler

    def described_handler(
        self,
        name: str = None,
        description: str = None,
        deprecated: bool = False,
        **other_meta: dict,
    ):
        def decorator(coro: typing.Callable):
            handler = self.get_handler(coro)
            if not handler:
                raise RuntimeError("Handler not registered.")
            meta = {
                "name": name,
                "description": description,
                "deprecated": deprecated,
                **other_meta,
            }
            if handler.coro.__doc__:  # or set description in docstring
                meta["description"] = handler.coro.__doc__.strip()
            handler.meta = {k: v for k, v in meta.items() if v is not None}

        return decorator

    def message_handler(
        self,
        *rules: typing.Tuple[typing.Type[BaseRule], typing.Callable, typing.Awaitable],
        commands: typing.Optional[typing.List[str]] = None,
        text: typing.Optional[str] = None,
        payload: typing.Optional[str] = None,
        chat_action: typing.Optional[types.message.Action] = None,
        data_check: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
        count_args: typing.Optional[int] = None,
        have_args: typing.Optional[
            typing.List[typing.Union[typing.Callable, typing.Awaitable]]
        ] = None,
        in_chat: typing.Optional[bool] = None,
        in_pm: typing.Optional[bool] = None,
        from_bot: typing.Optional[bool] = None,
        with_reply_message: typing.Optional[bool] = None,
        with_fwd_messages: typing.Optional[bool] = None,
        count_fwd_messages: typing.Optional[int] = None,
        **named_rules: typing.Dict[str, typing.Any],
    ):
        """
        Register message handler with decorator.

        standart named rules:
        :param commands:
        :param text:
        :param payload:
        :param chat_action:
        :param data_check:
        :param count_args:
        :param have_args:
        :param in_chat:
        :param in_pm:
        :param from_bot:
        :param with_reply_message:
        :param with_fwd_messages:
        :param count_fwd_messages:

        :param rules: other user rules
        :param named_rules: other user named rules
        :return:
        """
        standart_named_rules = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k != "coro"
            and k != "self"
            and k != "rules"
            and k != "named_rules"
        }

        def decorator(coro: typing.Callable):
            nonlocal rules, named_rules

            rules = list(rules)
            rules.extend(self.default_rules)
            named_rules.update(self.default_named_rules)
            named_rules.update(**standart_named_rules)

            self.handlers.append(
                HandlerInBlueprint(coro, Event.MESSAGE_NEW, rules, named_rules, {})
            )
            return coro

        return decorator

    def event_handler(
        self,
        event_type: Event,
        *rules: typing.Tuple[typing.Type[BaseRule]],
        **named_rules: typing.Dict[str, typing.Any],
    ):
        def decorator(coro: typing.Callable):
            nonlocal rules, named_rules

            rules = list(rules)
            rules.extend(self.default_rules)
            named_rules.update(self.default_named_rules)

            self.handlers.append(
                HandlerInBlueprint(coro, event_type, rules, named_rules, {})
            )
            return coro

        return decorator
