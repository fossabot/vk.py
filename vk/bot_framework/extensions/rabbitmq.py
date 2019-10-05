import logging

from ..dispatcher.extension import BaseExtension
from vk.constants import JSON_LIBRARY

logger = logging.getLogger(__name__)
try:
    import aio_pika
except ImportError:
    aio_pika = None


class RabbitMQ(BaseExtension):
    key = "rabbitmq"

    def __init__(
        self, vk, queue_name: str, rabbitmq_url: str = "amqp://guest:guest@127.0.0.1/"
    ):
        if aio_pika:
            self._vk = vk
            self._queue_name = queue_name
            self._url = rabbitmq_url
        else:
            raise RuntimeWarning(
                "Please install aio_pika (pip install aio_pika) for use this extension"
            )

    async def get_events(self) -> None:
        pass

    async def run(self, dp):
        logger.info("RabbitMQ consumer started!")
        connection = await aio_pika.connect_robust(self._url, loop=self._vk.loop)
        async with connection:

            channel: aio_pika.Channel = await connection.channel()

            queue: aio_pika.Queue = await channel.declare_queue(
                self._queue_name, auto_delete=True
            )

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        event = JSON_LIBRARY.loads(message.body.decode())
                        await dp._process_events(event)
