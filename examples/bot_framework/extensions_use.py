import logging

from vk import types
from vk import VK
from vk.bot_framework import Dispatcher
from vk.utils import TaskManager

logging.basicConfig(level="INFO")

bot_token = "123"
vk = VK(bot_token)
gid = 123
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)


@dp.message_handler(text="hello")
async def handle_event(message: types.Message, data: dict):
    await message.reply("Hello!")


async def run():
    from vk.bot_framework.extensions import RabbitMQ

    dp.setup_extension(RabbitMQ)
    dp.run_extension("rabbitmq", vk=vk, queue_name="test_queue")


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
