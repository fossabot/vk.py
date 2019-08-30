from vk import VK
from vk.utils import TaskManager

import asyncio
import logging

logging.basicConfig(level="DEBUG")

token = "TOKEN"
vk = VK(access_token=token)
task_manager = TaskManager(vk.loop)
api = vk.get_api()


async def send_message():
    resp = await api.messages.send(peer_id=1, message="hello!", random_id=0)
    print(resp)

if __name__ == "__main__":
    task_manager.add_task(send_message)
    task_manager.run()
    task_manager.close()  # close event loop manually
