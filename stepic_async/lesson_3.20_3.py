import asyncio


class TimeoutCondition(asyncio.Condition):
    def __init__(self):
        super().__init__()

    async def wait_for(self, predicate, timeout=None):
        try:
            async with asyncio.timeout(timeout):
                return await super().wait_for(predicate)
        except TimeoutError:
            return predicate()

