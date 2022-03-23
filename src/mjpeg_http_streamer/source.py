import abc
import asyncio
import os
import sys
from abc import abstractmethod

from mjpeg_http_streamer.arguments import SOURCE_STDIN, SOURCE_FIFO


class InputSource(abc.ABC):

    @abstractmethod
    async def read(self, n):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class StdinInputSource(InputSource):

    def __init__(self):
        self._reader = None

    async def read(self, n):
        return self._reader.read(n)

    async def __aenter__(self):
        self._reader = await create_pipe_reader(sys.stdin)
        return self


class FifoInputSource(InputSource):
    def __init__(self, fifo_path):
        self._fifo_path = fifo_path
        self._reader = None

    async def read(self, n):
        while True:
            if self._reader is None:
                self._reader = await self._open_fifo()

            data = await self._reader.read(n)
            if data:
                return data

            self._reader = None

    async def _open_fifo(self):
        return await create_pipe_reader(open(self._fifo_path, 'rb'))

    async def __aenter__(self):
        os.mkfifo(self._fifo_path, mode=0o600)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            os.remove(self._fifo_path)
        except FileNotFoundError:
            # if the fifo does not exist we have already reached the desired state
            pass


def create_input_source(args):
    source_type = args.source
    if source_type == SOURCE_STDIN:
        return StdinInputSource()
    elif source_type == SOURCE_FIFO:
        return FifoInputSource(args.fifo)

    raise ValueError(f"Unknown source type ${source_type}.")


async def create_pipe_reader(file_like_object):
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, file_like_object)
    return reader
