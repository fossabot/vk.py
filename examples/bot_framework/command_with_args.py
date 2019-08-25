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


@dp.message_handler(commands=["buy"], have_args=[lambda arg: arg.isdigit(), lambda arg: arg > 10])
async def handler(message: types.Message, data: dict):
    """
    Validate args. You may add to list lambda`s, or sync func`s with 1 arg (arg) and returned bool-like value.
    """
    await message.answer("Ok.")


@dp.message_handler(commands=["add"], count_args=2)
async def pretty_handler(message: types.Message, data: dict):
    """
    Not validate args. Only check len args (without command, =))
    """

    await message.answer("OK...")


async def run():
    await dp.run_polling()


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
