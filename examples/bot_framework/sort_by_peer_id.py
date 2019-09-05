from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher
from vk import types

import logging

logging.basicConfig(level="INFO")

bot_token = "123"
vk = VK(bot_token)
gid = 123
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)


@dp.message_handler(commands=["start"], from_bot=True)
async def handler(message: types.Message, data: dict):
    """
    Accept messages only from bots (from groups), from PM and etc.
    """
    await message.answer("Hello, group!")


@dp.message_handler(commands=["start"], in_pm=True)
async def pretty_handler(message: types.Message, data: dict):
    """
    Accept messages only from users (in personal messages (PM))
    """

    await message.answer("Hello, user!")


@dp.message_handler(commands=["start"], in_chat=True)
async def my_new_handler(message: types.Message, data: dict):
    """
    Accept messages only from chats. (from bots and users).
    """
    await message.answer("Hello, chat!")


async def run():
    dp.run_polling()


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
