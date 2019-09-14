import logging

from vk import types
from vk import VK
from vk.bot_framework import Dispatcher
from vk.bot_framework.dispatcher import Blueprint
from vk.types import BotEvent
from vk.utils import TaskManager

logging.basicConfig(level="DEBUG")

bot_token = "token"
vk = VK(bot_token)
gid = 123
task_manager = TaskManager(vk.loop)

dp = Dispatcher(vk, gid)


bp = Blueprint()


@bp.message_handler(text="hello")
async def handler(message: types.Message, data: dict):
    await message.answer("hello my friend!")


@bp.event_handler(BotEvent.WALL_POST_NEW)
async def handler_reply_new(event, data: dict):
    print(event)


async def run():
    dp.setup_blueprint(bp)
    dp.run_polling()


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=False)
