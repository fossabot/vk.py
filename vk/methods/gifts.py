from .base import BaseMethod
from vk.types.responses import gift as m

import typing
from typing import Union


class Gifts(BaseMethod):
    async def get(self, user_id: int = None, count: int = None, offset: int = None):
        """
        Returns a list of user gifts.
        :param user_id: User ID.
        :param count: Number of gifts to return.
        :param offset: Offset needed to return a specific subset of results.


        """
        method = self.get_method_name(self.get)
        params = self.create_params(locals())
        r = await self.api_request(method, params)
        return m.Get(**r)
