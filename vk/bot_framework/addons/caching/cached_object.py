import typing

from vk.types.base import BaseModel


class CachedResponse(BaseModel):
    """
    Return this object for cache response.
    """

    method_name: typing.AnyStr
    method_params: typing.Dict = {}
