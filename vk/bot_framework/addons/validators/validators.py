from vk import VK
from vk.exceptions import APIException
from vk.types import Message

vk = VK.get_current(no_error=False)
api = vk.get_api()


async def valid_id(arg: str, _: Message):
    """
    Validate passed in message ID.
    This validator just search user in VK which have this ID.
    :param _:
    :param arg:
    :return:
    """
    if not arg.isdigit():
        return False
    try:
        result = await vk.api_request("users.get", {"user_ids": arg})
    except APIException:
        return False
    return result


def positive_number(arg: str):
    """
    Validate passed in message digit.
    If digit is positive - returns true.
    :param arg:
    :return:
    """
    if not arg.isdigit():
        return False
    arg = int(arg)
    if arg <= 0:
        return False
    return True
