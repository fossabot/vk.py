import logging
import typing
from asyncio import iscoroutinefunction

from ..dispatcher.rule import BaseRule
from ..dispatcher.rule import NamedRule
from vk import types
from vk.constants import JSON_LIBRARY
from vk.types.message import Action

logger = logging.getLogger(__name__)

"""
Built-in rules.
"""


class Command(BaseRule):
    def __init__(self, command: str = None):
        self.prefix = "/"
        self.command: str = command

    async def check(self, message: types.Message, data: dict):
        msg = message.text.lower()
        result = f"{self.prefix}{self.command}" == msg
        logger.debug(f"Processing text of message. Text in message: {msg}")
        logger.debug(f"Result of Command rule: {result}")
        return result


class Text(NamedRule):
    key = "text"

    def __init__(self, text: str):
        self.text: str = text

    async def check(self, message: types.Message, data: dict):
        msg = message.text.lower()
        result = msg == self.text.lower()
        logger.debug(f"Processing text of message. Text in message: {msg}")
        logger.debug(f"Result of Text rule: {result}")
        return result


class Commands(NamedRule):
    key = "commands"

    def __init__(self, commands: typing.List[str]):
        self.commands = commands
        self.prefix = "/"

    async def check(self, message: types.Message, data: dict):
        passed = False
        msg = message.text.lower().split()[0]
        for command in self.commands:
            if msg == f"{self.prefix}{command}":
                passed = True
                break
        logger.debug(f"Processing text of message. Text in message: {msg}")
        logger.debug(f"Result of Commands rule: {passed}")
        return passed


class Payload(NamedRule):
    key = "payload"

    def __init__(self, payload: str):
        self.payload = payload

    async def check(self, message: types.Message, data: dict):
        if message.payload:
            payload = JSON_LIBRARY.loads(message.payload)
            result = payload == self.payload
            logger.debug(
                f"Processing payload of message. Payload in message: {payload}"
            )
            logger.debug(f"Result of Payload rule: {result}")
            return result


class ChatAction(NamedRule):
    key = "chat_action"

    def __init__(self, action: Action):
        self.action = action

    async def check(self, message: types.Message, data: dict):
        if message.action.type:
            action = Action(message.action.type)
            result = action is self.action
            logger.debug(f"Processing action of message. Action in message: {action}")
            logger.debug(f"Result of ChatAction rule: {result}")
            return result


class DataCheck(NamedRule):
    key = "data_check"

    def __init__(self, data: typing.Dict[str, typing.Any]):
        self.data = data  # for example: {"my_key": "my_value"}

    async def check(self, *args):
        data: dict = args[1]
        passed = True
        for key, value in self.data.items():
            value_data = data.get(key)
            if value_data != value:
                passed = False
                break
        logger.debug(f"Result of DataCheck rule: {passed}")
        return passed


class MessageCountArgs(NamedRule):
    """
    Get args and return result of equeal len(args) and passed args.
    """

    key = "count_args"

    def __init__(self, count_args: int):
        self.count_args = count_args

    async def check(self, message: types.Message, data: dict):
        count = len(message.get_args())
        result = count == self.count_args
        logger.debug(f"Received {count} args in message")
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
        count_args = len(args)
        count_validators = len(self.args_validators)
        if count_args != count_validators:
            logger.debug(
                f"Received {count_args} args in message. Passed validators {count_validators}"
            )
            logger.debug(f"Result of MessageArgsValidate rule: False")
            return False
        passed = True
        for validator, arg in zip(self.args_validators, args):
            if iscoroutinefunction(validator):
                result = await validator(arg)
            else:
                result = validator(arg)
            if not result:
                logger.debug("Result of MessageArgsValidate rule: False")
                return False
        logger.debug(f"Result of MessageArgsValidate rule: {passed}")
        return passed


class InChat(NamedRule):
    key = "in_chat"

    def __init__(self, in_chat: bool):
        self.in_chat: bool = in_chat

    async def check(self, message: types.Message, data: dict):
        result = self.in_chat is bool(message.peer_id >= 2e9)
        logger.debug(f"Received peer_id: {message.peer_id}")
        logger.debug(f"Result of InChat rule: {result}")

        return result


class InPersonalMessages(NamedRule):
    key = "in_pm"

    def __init__(self, in_pm: bool):
        self.in_pm: bool = in_pm

    async def check(self, message: types.Message, data: dict):
        result = self.in_pm is bool(message.peer_id < 2e9)
        logger.debug(f"Received peer_id: {message.peer_id}")
        logger.debug(f"Result of InPersonalMessages rule: {result}")

        return result


class FromBot(NamedRule):
    key = "from_bot"

    def __init__(self, from_bot: bool):
        self.from_bot: bool = from_bot

    async def check(self, message: types.Message, data: dict):
        result = self.from_bot is bool(message.from_id < 0)
        logger.debug(f"Received from_id: {message.from_id}")
        logger.debug(f"Result of FromBot rule: {result}")

        return result


class WithReplyMessage(NamedRule):
    key = "with_reply_message"

    def __init__(self, with_reply_message: bool):
        self.with_reply_message: bool = with_reply_message

    async def check(self, message: types.Message, data: dict):
        logger.debug(f"Result of WithReplyMessage rule: {bool(message.reply_message)}")
        return bool(message.reply_message)


class WithFwdMessages(NamedRule):
    key = "with_fwd_messages"

    def __init__(self, with_fwd_messages: bool):
        self.with_reply_message: bool = with_fwd_messages

    async def check(self, message: types.Message, data: dict):
        logger.debug(f"Result of WithFwdMessages rule: {bool(message.fwd_messages)}")
        return bool(message.fwd_messages)


class CountFwdMessages(NamedRule):
    key = "count_fwd_messages"

    def __init__(self, count_fwd_messages: int):
        self.count_fwd_messages: int = count_fwd_messages

    async def check(self, message: types.Message, data: dict):
        count = len(message.fwd_messages)
        result = count == self.count_fwd_messages
        logger.debug(f"Received fwd_messages: {count}")
        logger.debug(f"Result of CountFwdMessages rule: {result}")
        return result
