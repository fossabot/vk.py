import logging

from vk import types
from vk import VK
from vk.bot_framework import Dispatcher
from vk.bot_framework import Storage
from vk.utils import TaskManager

logging.basicConfig(level="INFO")

bot_token = "123"
vk = VK(bot_token)
gid = 123
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)
storage = Storage()
dp.storage = storage

really_needed_counter = 0

dp.storage.place("really_needed_counter", really_needed_counter)


@dp.message_handler(text="hello")
async def handle_event(message: types.Message, data: dict):
    c = dp.storage.get("really_needed_counter", 0)
    await message.answer(f"Hello! {c}")
    dp.storage.update("really_needed_counter", c + 1)


async def run():
    dp.run_polling()


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
