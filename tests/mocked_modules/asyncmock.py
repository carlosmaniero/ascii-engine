import asyncio
from unittest.mock import MagicMock


class AsyncMock(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wait_future = asyncio.Future()

    async def __call__(self, *args, **kwargs):
        self.wait_future.set_result(True)
        return super().__call__(*args, **kwargs)

    async def wait_for_call(self, timeout=1):
        return await asyncio.wait_for(self.wait_future, timeout)
