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
        result = text == self.text.lower()
        logger.debug(f"Result of Text rule: {result}")
        return result


class Commands(NamedRule):
    key = "commands"

    def __init__(self, commands: typing.List[str]):
        self.commands = commands
        self.prefix = "/"

    async def check(self, message: types.Message, data: dict):
        text = message.text.lower().split()[0]
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
        _passed = True
        for key, value in self.data.items():
            value_data = data.get(key)
            if value_data != value:
                _passed = False
                break
        logger.debug(f"Result of DataCheck rule: {_passed}")
        return _passed


class MessageCountArgs(NamedRule):
    """
    Get args and return result of equeal len(args) and passed args.
    """

    key = "count_args"

    def __init__(self, count_args: int):
        self.count_args = count_args

    async def check(self, message: types.Message, data: dict):
        args = message.get_args()
        result = len(args) == self.count_args
        logger.debug(f"Result of MessageCountArgs rule: {result}")
        return result


class MessageArgsValidate(NamedRule):
    """
    Get and validate args by passed validators.
    """

    key = "have_args"

    def __init__(self, args_validators: typing.List[typing.Callable]):
        self.args_validators = args_validators

    async def check(self, message: types.Message, data: dict):
        args = message.get_args()
        if len(args) != len(self.args_validators):
            return False
        _passed = True
        for arg in args:
            for validator in self.args_validators:
                result = validator(arg)
                if not result:
                    _passed = False
                    logger.debug(f"Result of MessageArgsValidate rule: {_passed}")
                    return _passed
        if _passed:
            logger.debug(f"Result of MessageArgsValidate rule: {_passed}")
            return _passed


class InChat(NamedRule):
    key = "in_chat"

    def __init__(self, in_chat: bool):
        self.in_chat: bool = in_chat

    async def check(self, message: types.Message, data: dict):
        result = self.in_chat is bool(message.peer_id >= 2e9)
        logger.debug(f"Result of InChat rule: {result}")

        return result


class InPersonalMessages(NamedRule):
    key = "in_pm"

    def __init__(self, in_pm: bool):
        self.in_pm: bool = in_pm

    async def check(self, message: types.Message, data: dict):
        result = self.in_pm is bool(message.peer_id < 2e9)
        logger.debug(f"Result of InPersonalMessages rule: {result}")

        return result


class FromBot(NamedRule):
    key = "from_bot"

    def __init__(self, from_bot: bool):
        self.from_bot: bool = from_bot

    async def check(self, message: types.Message, data: dict):
        result = self.from_bot is bool(message.from_id < 0)
        logger.debug(f"Result of FromBot rule: {result}")

        return result


class WithReplyMessage(NamedRule):
    key = "with_reply_message"

    def __init__(self, with_reply_message: bool):
        self.with_reply_message: bool = with_reply_message

    async def check(self, message: types.Message, data: dict):
        logger.debug(f"Result of WithReplyMessage rule: {message.reply_message}")
        return message.reply_message
