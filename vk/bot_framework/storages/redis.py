import asyncio
import typing

from ..dispatcher.storage import AbstractAsyncStorage

try:
    import aioredis  # noqa
except ImportError:
    aioredis = None
    raise RuntimeError("For use this storage install aioredis (pip install aioredis)")


class RedisStorage(AbstractAsyncStorage):
    def __init__(
        self,
        address: str,
        loop: asyncio.AbstractEventLoop,
        db: str = None,
        password: str = None,
    ):
        self._address = address
        self._db = db
        self._password = password
        self._loop = loop
        self.connection: typing.Optional[aioredis.Redis] = None

    async def create_connection(self) -> aioredis.Redis:
        if not self.connection:
            conn: aioredis.Redis = await aioredis.create_redis(
                address=self._address,
                db=self._db,
                password=self._password,
                loop=self._loop,
            )
            self.connection = conn
            return conn
        else:
            raise RuntimeError("Connection already setuped")

    async def place(
        self, key: typing.AnyStr, value: typing.Any, expire=0, pexpire=0
    ) -> None:
        await self.connection.set(key, value)

    async def get(
        self, key: typing.AnyStr, default: typing.Any = None
    ) -> typing.Optional[typing.Any]:
        value = await self.connection.get(key)
        if value is None:
            return default
        return value.decode()

    async def update(self, key: typing.AnyStr, value: typing.Any, expire=0, pexpire=0):
        await self.place(key, value, expire, pexpire)

    async def delete(
        self, key: typing.AnyStr, *keys: typing.Tuple[typing.AnyStr]
    ) -> None:
        await self.connection.delete(key, *keys)

    async def exists(
        self, key: typing.AnyStr, *keys: typing.Tuple[typing.AnyStr]
    ) -> bool:
        result = await self.connection.exists(key, *keys)
        if result == 0:
            return False
        else:
            return True
