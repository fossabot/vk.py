import logging
import typing

from vk import VK
from vk.utils import TaskManager

logging.basicConfig(level="DEBUG")

token = "TOKEN"
vk = VK(access_token=token)
task_manager = TaskManager(vk.loop)

error_dp = vk.error_dispatcher


@error_dp.error_handler(error_code=1)
async def handler(error: typing.Dict):
    logging.info("Exception with code '1' handled!")


async def status_get():
    resp = await vk.api_request("status.get")
    print(resp)


if __name__ == "__main__":
    task_manager.add_task(status_get)
    task_manager.run()
    task_manager.close()  # close event loop manually
