import asyncio
from abc import ABC, abstractmethod


class StreamProvider(ABC):

    @abstractmethod
    async def read(self):
        pass

    @abstractmethod
    async def tick(self):
        pass


class InstantStreamProvider(StreamProvider):

    def __init__(self, source):
        self._source = source

    async def read(self):
        return await self._source.read(1024)

    async def tick(self):
        pass


class ClockedStreamProvider(StreamProvider):

    def __init__(self, source, interval):
        self._source = source
        self._interval = interval

    async def read(self):
        return await self._source.read(1024)

    async def tick(self):
        await asyncio.sleep(self._interval)
