import logging
import typing
from asyncio import iscoroutinefunction

from vk.bot_framework.dispatcher.rule import BaseRule
from vk.types.events.community.events_list import Event

logger = logging.getLogger(__name__)


class SkipHandler(Exception):
    """
    Raise this which you want skip handlers.
    """

    pass


class Handler:
    def __init__(
        self, event_type: Event, handler: typing.Callable, rules: typing.List[BaseRule]
    ):
        """

        :param event_type: type of event which this handler accepted
        :param handler: coroutine
        :param rules: list of rules which be executed
        """
        self.event_type: Event = event_type
        self.handler: typing.Callable = handler
        self.rules: typing.List[BaseRule] = rules

    async def execute_handler(self, *args):
        """
        Execute rules and handler
        :param args:
        :return:
        """
        # args - (event, data)
        if self.rules:
            _execute = False
            ctx_handler_data = {}
            for rule in self.rules:
                if not iscoroutinefunction(rule):
                    result = rule(*args)
                else:
                    result = await rule(*args)
                if not result:
                    _execute = False
                    break
                if isinstance(result, dict):
                    ctx_handler_data.update(result)
                _execute = True

            if _execute:
                args[1].update(ctx_handler_data)
                await self.handler(*args)
                return True
        else:
            await self.handler(*args)
            return True
