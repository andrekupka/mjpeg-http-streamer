class MJPEGStreamReader:

    def __init__(self, stream_provider, output_queue):
        self._start_symbol = b"\xff\xd8"
        self._end_symbol = b"\xff\xd9"
        self._stream_provider = stream_provider
        self._output_queue = output_queue

        self._found_frame = False
        self._current_index = 0
        self._buffer = b""

    async def run(self):
        while True:
            data = await self._stream_provider.read()
            if not data:
                await self._output_queue.put(None)
                return

            self._buffer += data

            while True:
                if not self._found_frame:
                    try:
                        index = self._buffer.index(self._start_symbol)
                        self._buffer = self._buffer[index:]
                        self._found_frame = True
                    except ValueError:
                        characters_to_keep = min(len(self._buffer), len(self._start_symbol)-1)
                        self._buffer = self._buffer[-characters_to_keep:]
                        break
                    finally:
                        self._current_index = 0

                try:
                    index = self._buffer[self._current_index:].index(self._end_symbol) + self._current_index
                    frame_end_index = index + len(self._end_symbol)
                    # publish frame
                    frame = self._buffer[0:frame_end_index]
                    await self._output_queue.put(frame)
                    await self._stream_provider.tick()

                    self._buffer = self._buffer[frame_end_index:]
                    self._current_index = 0
                except ValueError:
                    self._current_index = max(0, len(self._buffer) - len(self._end_symbol))
                    break
