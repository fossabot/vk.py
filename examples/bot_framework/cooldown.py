import logging

from vk import types
from vk import VK
from vk.bot_framework import Dispatcher
from vk.bot_framework.addons import cooldown
from vk.bot_framework.storages import TTLDictStorage
from vk.utils import TaskManager

logging.basicConfig(level="INFO")

bot_token = "123"
vk = VK(bot_token)
gid = 123
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)
storage = TTLDictStorage()  # in RAM
cooldown.set_cooldown_message(
    "Oh... Please wait {cooldown} seconds..."
)  # or use standart message


@dp.message_handler(text="text")
@cooldown.cooldown_handler(
    storage, cooldown_time=10, for_specify_user=True
)  # have a simply design
async def test(msg: types.Message, data):
    await msg.answer("Hello!")


async def run():
    dp.run_polling()


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
