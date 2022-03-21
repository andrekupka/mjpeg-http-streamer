class MJPEGStreamReader:

    def __init__(self, stream_provider, output_queue):
        self._start_symbol = b"\xff\xd8"
        self._end_symbol = b"\xff\xd9"
        self._stream_provider = stream_provider
        self._output_queue = output_queue

        self._frame_start = None
        self._frame_end = None
        self._buffer = b""

    async def run(self):
        while True:
            data = await self._stream_provider.read()
            if not data:
                await self._output_queue.put(None)
                return

            self._buffer += data

            while True:
                if self._frame_start is None:
                    try:
                        index = self._buffer.index(self._start_symbol)
                        self._frame_start = index
                    except ValueError:
                        self._buffer = b""
                        break

                if self._frame_start is not None and self._frame_end is None:
                    try:
                        index = self._buffer.index(self._end_symbol)
                        self._frame_end = index
                    except ValueError:
                        break

                if self._frame_start is not None and self._frame_end is not None:
                    frame = self._buffer[self._frame_start:self._frame_end + len(self._end_symbol)]
                    await self._output_queue.put(frame)
                    await self._stream_provider.tick()
                    self._buffer = self._buffer[self._frame_end + len(self._end_symbol):]
                    self._frame_start = None
                    self._frame_end = None
