from vk import VK
from vk.exceptions import APIException
from vk.types import Message
from vk.types import User


validators_answers: dict = {"valid_vkid": "", "positive_number": ""}


async def valid_vkid(arg: str, message: Message):
    """
    Validate passed in message ID.
    This validator just search user in VK which have this ID.

    If all good - append to data received response from VKAPI in field 'valid_id_user'.
    Example:

    @dp.message_handler(commands=["hello"], have_args=[validators.valid_vkid])
    async def handle(message: types.Message, data: dict):
        usr: types.User = data["valid_vkid_user"]
        await message.answer(usr.first_name)
    :param message:
    :param arg:
    :return:
    """
    vk = VK.get_current()
    have_answer = validators_answers["valid_vkid"]
    if not arg.isdigit():
        if have_answer:
            await message.answer(have_answer)
        return False
    try:
        result = await vk.api_request("users.get", {"user_ids": arg})
    except APIException:
        if have_answer:
            await message.answer(have_answer)
        return False
    if not result and have_answer:
        await message.answer(have_answer)
    if result:
        return {"valid_vkid_user": User(**result[0])}
    return result


async def positive_number(arg: str, message: Message):
    """
    Validate passed in message digit.
    If digit is positive - returns true.
    :param message:
    :param arg:
    :return:
    """
    have_answer = validators_answers["positive_number"]
    if not arg.isdigit():
        if have_answer:
            await message.answer(have_answer)
        return False
    if int(arg) <= 0:
        if have_answer:
            await message.answer(have_answer)
        return False
    return True
