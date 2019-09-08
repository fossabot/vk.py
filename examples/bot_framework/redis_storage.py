import logging

from vk import types
from vk import VK
from vk.bot_framework import Dispatcher
from vk.bot_framework.storages import RedisStorage
from vk.utils import TaskManager

logging.basicConfig(level="INFO")

bot_token = "123"
vk = VK(bot_token)
gid = 123
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)
storage: RedisStorage = RedisStorage("redis://localhost", vk.loop)

dp.storage = storage


@dp.message_handler(text="hello")
async def handle_event(message: types.Message, data: dict):
    c = await dp.storage.get("really_needed_counter", 0)
    await message.answer(f"Hello! {c}")
    await dp.storage.update("really_needed_counter", int(c) + 1)


async def run():
    await dp.storage.create_connection()
    await dp.storage.place("really_needed_counter", 1)
    dp.run_polling()


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
