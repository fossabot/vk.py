from ..dispatcher.rule import NamedRule, BaseRule
from vk.types.message import Action
from vk.constants import JSON_LIBRARY

from vk import types

import typing
import logging

logger = logging.getLogger(__name__)

"""
Built-in rules.
"""


class Command(BaseRule):
    def __init__(self, command: str = None):
        self.prefix = "/"
        self.command: str = command

    async def check(self, message: types.Message, data: dict):
        text = message.text.lower()
        result = f"{self.prefix}{self.command}" == text
        logger.debug(f"Result of Command rule: {result}")
        return result


class Text(NamedRule):
    key = "text"

    def __init__(self, text: str):
        self.text: str = text

    async def check(self, message: types.Message, data: dict):
        text = message.text.lower()
        result = text == self.text
        logger.debug(f"Result of Text rule: {result}")
        return result


class Commands(NamedRule):
    key = "commands"

    def __init__(self, commands: typing.List[str]):
        self.commands = commands
        self.prefix = "/"

    async def check(self, message: types.Message, data: dict):
        text = message.text.lower()
        _accepted = False
        for command in self.commands:
            if text == f"{self.prefix}{command}":
                _accepted = True
        logger.debug(f"Result of Commands rule: {_accepted}")
        return _accepted


class Payload(NamedRule):
    key = "payload"

    def __init__(self, payload: str):
        self.payload = payload

    async def check(self, message: types.Message, data: dict):
        payload = message.payload
        if payload:
            payload = JSON_LIBRARY.loads(payload)
            result = payload == self.payload
            logger.debug(f"Result of Payload rule: {result}")
            return result


class ChatAction(NamedRule):
    key = "chat_action"

    def __init__(self, action: Action):
        self.action = action

    async def check(self, message: types.Message, data: dict):
        action = message.action.type
        if action:
            action = Action(action)
            result = action is self.action
            logger.debug(f"Result of ChatAction rule: {result}")
            return result


class DataCheck(NamedRule):
    key = "data_check"

    def __init__(self, data: typing.Dict[str, typing.Any]):
        self.data = data  # for example: {"my_key": "my_value"}

    async def check(self, *args):
        data: dict = args[1]
        key = list(self.data.keys())[0]
        result = data.get(key) == self.data[key]
        logger.debug(f"Result of DataCheck rule: {result}")
        return result
