"""
A file which contains all project constants.
"""

API_VERSION: str = "5.101"  # current api version https://vk.com/dev/versions
API_LINK: str = "https://api.vk.com/method/"  # link to access API

try:
    import ujson as json  # noqa
except ImportError:
    import json
JSON_LIBRARY = json


def default_rules() -> dict:
    """
    Build and return dict of default handlers rules.
    :return:
    """
    from vk.bot_framework.rules.rules import (
        Commands,
        Text,
        Payload,
        ChatAction,
        DataCheck,
        MessageCountArgs,
        MessageArgsValidate,
        InPersonalMessages,
        InChat,
        FromBot,
        WithReplyMessage,
    )

    _default_rules = {
        "commands": Commands,
        "text": Text,
        "payload": Payload,
        "chat_action": ChatAction,
        "data_check": DataCheck,
        "count_args": MessageCountArgs,
        "have_args": MessageArgsValidate,
        "in_chat": InChat,
        "in_pm": InPersonalMessages,
        "from_bot": FromBot,
        "with_reply_message": WithReplyMessage,
    }
    return _default_rules


def default_extensions() -> dict:
    """
    Build and return dict of default dispatcher extensions
    :return:
    """
    from vk.bot_framework.extensions import Polling

    _default_extensions = {"polling": Polling}

    return _default_extensions
