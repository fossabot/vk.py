import asyncio
import concurrent.futures
import typing


class BackgroundTask:
    def __init__(
        self,
        async_or_sync: typing.Union[typing.Awaitable, typing.Callable],
        *async_or_sync_args
    ):
        """
        Run task in background.
        If task is synchronous his will running in ThreadPoolExecutor.
        :param async_or_sync:
        :param async_or_sync_args:
        """
        self._async_or_sync = async_or_sync
        self._async_or_sync_args = async_or_sync_args
        self.is_async = asyncio.iscoroutinefunction(async_or_sync)

        self._pool = concurrent.futures.ThreadPoolExecutor()

    async def __call__(self):
        await self.__run()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def __run(self) -> None:
        loop = asyncio.get_running_loop()
        if self.is_async:
            if self._async_or_sync_args:
                loop.create_task(self._async_or_sync(*self._async_or_sync_args))
            else:
                loop.create_task(self._async_or_sync())
            return
        if self._async_or_sync_args:
            loop.run_in_executor(
                self._pool, self._async_or_sync, self._async_or_sync_args
            )
        else:
            loop.run_in_executor(self._pool, self._async_or_sync)
