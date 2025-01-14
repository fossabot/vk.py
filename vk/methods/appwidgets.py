from .base import BaseMethod
from vk.types.responses import appwidgets as m

import typing
from typing import Union


class AppWidgets(BaseMethod):
    async def update(self, code: str = None, type: str = None):
        """
        Allows to update community app widget
        :param code:
        :param type:


        """
        method = self.get_method_name(self.update)
        params = self.create_params(locals())
        r = await self.api_request(method, params)
        return m.Update(**r)
