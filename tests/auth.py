import sys

sys.path.append("..")

import pytest
from vk import VK, exceptions


@pytest.mark.asyncio
async def bad_auth(bad_token: str):
    vk = VK(bad_token)
    await vk.api_request("status.get", {})
    return vk


@pytest.mark.xfail(raises=exceptions.APIException)
@pytest.mark.asyncio
async def test_auth():
    vk = await bad_auth("bad_token")

